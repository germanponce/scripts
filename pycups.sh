#! /usr/bin/env python
import cups
import time
import subprocess

main = 1
while main == 1:
   
    conn = cups.Connection()
                        
            #------Check Printer------------
    printers = conn.getPrinters()
    for printer in printers:
                    print printer,
                    printers[printer]['device-uri']
    printer_name = printers.keys()[1]
            #------------------------------ Star_TSP654_ ----
    time.sleep(0.1)
    filename = '/home/german/point_of_sale.report_receipt.pdf'
    printid = conn.printFile(printer_name,filename,'Python_Status_print' ,{})
    time.sleep(5)
    stop =0
    TIMEOUT =5
    while str(subprocess.check_output(['lpstat'])).find(str(printid)) > 0 and stop < TIMEOUT:
                    stop+- 1
                    time.sleep(0.5)
    if stop < TIMEOUT:
                    print 'Print success'
    else:
                    print 'Print FAILURE'
    time.sleep(1)
    print 'Thank You' 
    main = 0
