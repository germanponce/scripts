voucher_obj = self.pool.get('account.voucher')
voucher_line_obj = self.pool.get('account.voucher.line')
cr.execute("""
    select voucher_id from account_voucher_line group by voucher_id;
    """)
cr_res = cr.fetchall()
voucher_created_ids = [x[0] for x in cr_res if x]
voucher_ids = voucher_obj.search(cr, uid, [('id','not in',tuple(voucher_created_ids))])
# voucher_customers = voucher_obj.search(cr, uid, [('type','=','receipt')])
for voucher in voucher_obj.browse(cr, uid, voucher_ids, context):
    partner_id = voucher.partner_id.id
    journal_id = voucher.journal_id.id
    ttype = voucher.type
    date = voucher.date
    amount = voucher.amount
    currency_id = voucher.currency_id.id
    if not voucher.move_id:
        continue
    if ttype == 'receipt':
        if voucher.line_cr_ids:
            continue
    else:
        if ttype == 'payment':
            if voucher.line_dr_ids:
                continue
    if not journal_id:
        continue
    if context is None:
        context = {}
    #TODO: comment me and use me directly in the sales/purchases views
    res = voucher_obj.basic_onchange_partner(cr, uid, ids, partner_id, journal_id, ttype, context=context)
    if ttype in ['sale', 'purchase']:
        # return res
        continue
    ctx = context.copy()
    # not passing the payment_rate currency and the payment_rate in the context but it's ok because they are reset in recompute_payment_rate
    ctx.update({'date': date})
    vals = voucher_obj.recompute_voucher_lines(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=ctx)
    vals2 = voucher_obj.recompute_payment_rate(cr, uid, ids, vals, currency_id, date, ttype, journal_id, amount, context=context)
    for key in vals.keys():
        res[key].update(vals[key])
    values = vals2['value']
    if 'line_cr_ids' in values:
        cr.execute("""
            select account_id from account_move_line where move_id = %s
            """ % voucher.move_id.id)
        cr_res = cr.fetchall()
        account_ids = [x[0] for x in cr_res if x]
        line_cr_ids = values['line_cr_ids']
        for cre in line_cr_ids:
            if type(cre) == type({}):
                account_id = cre['account_id']
                if account_id in account_ids:
                    cre.update({'voucher_id':voucher.id})
                    voucher_line_id = voucher_line_obj.create(cr, uid, cre, context)
            # cr.execute("""
            #     update account_voucher_line
            #     set voucher_id = %s ;
            #     """ % voucher_line_id)
    if 'line_dr_ids' in values:
        cr.execute("""
            select account_id from account_move_line where move_id = %s
            """ % voucher.move_id.id)
        cr_res = cr.fetchall()
        account_ids = [x[0] for x in cr_res if x]
        line_dr_ids = values['line_dr_ids']
        for dr in line_dr_ids:
            if type(cre) == type({}):
                account_id = dr['account_id']
                if account_id in account_ids:
                    dr.update({'voucher_id':voucher.id})
                    voucher_line_id = voucher_line_obj.create(cr, uid, dr, context)
