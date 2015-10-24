####### Variables Globales para Oerplip, Base de Datos de Odoo, Usuario y Pass de la Base de Odoo para Admin ########
### Puerto de conexion tambien de Odoo

import oerplib
from oerplib import rpc

oerp_server = 'localhost'
oerp_protocol = 'xmlrpc'
oerp_port = 8069
oerp_user = 'admin'
oerp_passwd = '4dm1n..'
oerp_database = 'XMH23102015'
# oerp_passwd = 'admin'
# oerp_database = 'ARGILFACTURAE_PRUEBAS'
#oerp_port = 9069


oerp = oerplib.OERP(server=oerp_server, protocol=oerp_protocol, port=oerp_port)
user = oerp.login(user=oerp_user, passwd=oerp_passwd, database=oerp_database)

# location_id = oerp.get('stock.location').search([('name','=','PRODUCTO TERMINADO')])
# product_read = oerp.read('product.product', product_ids, ['name','list_price','stock_available','default_code'])
# mrp_ids = oerp.search('mrp.production', [('date_planned','>=',tz_date_1),('date_planned','<=',tz_date_2)])

voucher_obj = self.pool.get('account.voucher')
voucher_line_obj = self.pool.get('account.voucher.line')
move_line_obj = self.pool.get('account.move.line')
cr.execute("""
    select voucher_id from account_voucher_line group by voucher_id;
    """)
cr_res = cr.fetchall()
voucher_created_ids = [x[0] for x in cr_res if x]
voucher_ids = voucher_obj.search(cr, uid, [('id','not in',tuple(voucher_created_ids))])
# voucher_customers = voucher_obj.search(cr, uid, [('type','=','receipt')])
for voucher in voucher_obj.browse(cr, uid, voucher_ids, context):
    voucher_number = voucher.number
    voucher_amount = voucher.amount
    voucher_oerp_ids = oerp.get('account.voucher').search(
        [('number','=',voucher_number),('amount','=',voucher_amount)])
    if voucher_oerp_ids:
        for voucher_oerp in oerp.get('account.voucher').browse(voucher_oerp_ids):
            for cre in voucher_oerp.line_cr_ids:
                move_line_id = move_line_obj.search(cr, uid, [('id','=',cre.move_line_id.id)])
                if cre.move_line_id and move_line_id:
                    vals = {
                    'amount_unreconciled': cre.amount_unreconciled,
                    'move_line_id': cre.move_line_id.id,
                    'voucher_id': voucher.id,
                    'reconcile': cre.reconcile,
                    'create_date': cre.create_date if cre.create_date else False,
                    'account_id': cre.account_id.id if cre.account_id else False,
                    'currency_id': cre.currency_id.id if cre.currency_id else False,
                    'type': cre.type,
                    'partner_id': cre.partner_id.id if cre.partner_id else False,
                    # 'date': cre.date,
                    'date_due': cre.date_due,
                    'amount': cre.amount,
                    'untax_amount': cre.untax_amount,
                    'amount_original': cre.amount_original,
                    }
                    voucher_line_id = voucher_line_obj.create(cr, uid, vals, context)

            for dr in voucher_oerp.line_dr_ids:
                move_line_id = move_line_obj.search(cr, uid, [('id','=',dr.move_line_id.id)])
                if dr.move_line_id and move_line_id:
                    vals = {
                    'amount_unreconciled': dr.amount_unreconciled,
                    'move_line_id': dr.move_line_id.id,
                    'voucher_id': voucher.id,
                    'reconcile': dr.reconcile,
                    'create_date': dr.create_date if dr.create_date else False,
                    'account_id': dr.account_id.id if dr.account_id else False,
                    'currency_id': dr.currency_id.id if dr.currency_id else False,
                    'type': dr.type,
                    'partner_id': dr.partner_id.id if dr.partner_id else False,
                    # 'date': dr.date,
                    'date_due': dr.date_due,
                    'amount': dr.amount,
                    'untax_amount': dr.untax_amount,
                    'amount_original': dr.amount_original,
                    }
                    voucher_line_id = voucher_line_obj.create(cr, uid, vals, context)
