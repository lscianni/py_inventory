#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Louis Scianni

"""
Reference other tables for more robust search results
"""

import MySQLdb as mdb
import getpass
from sys import argv

item_table = 'items'
user_table = 'users'
chk_equip = 'checked_out_items'

unknown_sel = '\nNot a valid selection!\n'

try:
    server = argv[1]
    username = argv[2]
    passwd = getpass.getpass()
    db = argv[3]
except IndexError:
    server = input('Host: ')
    username = input('Username: ')
    passwd = getpass.getpass()
    db = input('DataBase: ')
    
    
try:
    con = mdb.connect(server, username, passwd, db)
        
except mdb.Error as e:
    print("Error: %s" % e)

cur = con.cursor()

def db_insert(sql):
    try:
        cur.execute(sql) 
        con.commit()
        print('succsess!')
       
    except mdb.Error as e:
                print('Failed to create record\nRolling back...')
                print("Error: %s" % e)
                con.rollback()
                
def db_select_simple(sql):
    try:    
        cur.execute(sql)
        row = cur.fetchone()
        print(str(row))
            
    except mdb.Error as e:
        print('Error: %s' % e)
                
def db_select(sql):
    try:    
        cur.execute(sql)
        
        for i in range(cur.rowcount):        # Fetch rows one by one using the fetchone() method. The row count property gives the number of rows returned by the SQL statement
            row = cur.fetchone()
            print(str(row))
            
    except mdb.Error as e:
        print('Error: %s' % e)
        
def check_avail(check_avail_sql):
    try:
        cur.execute(check_avail_sql)
        data = cur.fetchall()
        data = str(data).strip("(),'")
        
        if data.lower() == 'no':
            raise Exception('Item not available')
    except mdb.Error as e:
        print('Error: %s' % e)        
             
# Prompt
sel = True
while sel:

    print('\nATR Inventory Menu')
    print('1) List inventory') 
    print('2) List users')
    print('3) Check out equipment')
    print('4) Check in equipment (wip)')
    print('5) Add equipment (wip)')
    print('6) Add user (wip)')
  
    sel = input('>> ')
            
    if sel == '1':    # add sub menu for search refinement
        print('Item search')
        print('1) list all items')
        print('2) list items by type')
        print('3) search by serial')
        print('4) search by item id')
        print('5) list available items')
        print('6) search checked out items')
        item_results = 'id,type,make,model,serial,available'
        sel_items = input('>>> ')
        
        if sel_items == '1':
            print('\nListing all items\n')
            sql = 'SELECT %s FROM %s;' % (item_results, item_table)
            
        elif sel_items == '2':
            search_term = input('Item Type: ')
            print('\nListing items with type: %s\n' % search_term)
            if search_term.lower() == 'laptop':
                sql = 'SELECT %s FROM %s WHERE type = "Laptop";' % (item_results, item_table)
                
            if search_term.lower() == 'desktop':
                sql = 'SELECT %s FROM %s WHERE type = "Desktop";' % (item_results, item_table)
                
            if search_term.lower() == 'monitor':
                sql = 'SELECT %s FROM %s WHERE type = "Monitor";' % (item_results, item_table)
                
            if search_term.lower() == 'phone':
                sql = 'SELECT %s FROM %s WHERE type = "Phone";' % (item_results, item_table)

            if search_term.lower() == 'firewall':
                sql = 'SELECT %s FROM %s WHERE type = "Firewall";' % (item_results, item_table)
                
            if search_term.lower() == 'printer':
                sql = 'SELECT %s FROM %s WHERE type = "Printer";' % (item_results, item_table)
                
            if search_term.lower() == 'projector':
                sql = 'SELECT %s FROM %s WHERE type = "Projector";' % (item_results, item_table)
                
            if search_term.lower() == 'router':
                sql = 'SELECT %s FROM %s WHERE type = "Router";' % (item_results, item_table)
                
            if search_term.lower() == 'scanner':
                sql = 'SELECT %s FROM %s WHERE type = "Scanner";' % (item_results, item_table)

            if search_term.lower() == 'switch':
                sql = 'SELECT %s FROM %s WHERE type = "Switch";' % (item_results, item_table)
                
            if search_term.lower() == 'tv':
                sql = 'SELECT %s FROM %s WHERE type = "TV";' % (item_results, item_table)
                
            if search_term.lower() == 'ups':
                sql = 'SELECT %s FROM %s WHERE type = "UPS";' % (item_results, item_table)
                
            if search_term.lower() == 'modem':
                sql = 'SELECT %s FROM %s WHERE type = "Modem";' % (item_results, item_table)
           

        elif sel_items == '3':
            serial = input('serial number: ').upper()
            print('\nSearching for %s\n' % serial)
            sql = 'SELECT %s FROM %s WHERE serial = "%s";' % (item_results,item_table,serial)
                
        elif sel_items == '4':
            item_id = int(input('item id: '))
            print('\nSearching for item_id %d\n' % item_id)
            sql = 'SELECT %s FROM %s WHERE id = %d;' % (item_results, item_table, item_id)

        elif sel_items == '5':
            print('\nListing available items\n')
            sql = 'SELECT %s FROM %s WHERE available = "yes";' % (item_results, item_table)

        elif sel_items == '6':
            print('\nListing unavailable items\n')
            sql = 'SELECT id FROM %s WHERE available = "no";' % item_table
            db_select(sql)
            item_id = int(input('\nenter item id: '))
            sql = 'SELECT equip_id,type,checkout_date,return_date,date_returned,equip_id,type,make,model,serial,user_id FROM checked_out_items LEFT JOIN items ON checked_out_items.equip_id = items.id WHERE items.id = %d;' % item_id
            try:
                cur.execute(sql)
            except mdb.Error as e:
                print('SQL Error: %s' % e)
                con.rollback()
            

        else:
            print(unknown_sel)

        db_select(sql)
  
    elif sel == '2':
        print('User search')
        print('1) list all users')
        print('2) search by user id')
        print('3) search by name')
        print('4) list checked out items by user')
        
        sel_user = input('>>>')
        
        print('\nUser Listing\n')

        if sel_user == '1':
            sql = 'SELECT * FROM %s;' % user_table
            
        elif sel_user == '2':
            user_id = int(input('user id: '))
            print('\nSearching for user_id %d\n' % user_id)
            sql = 'SELECT * FROM %s WHERE id = "%d";' % (user_table, user_id)
            
        elif sel_user == '3':
            user_name = input('user name: ') 
            print('\nSearching for name: %s\n' % user_name)
            sql = 'SELECT * FROM users WHERE first_name = "{0}" OR last_name = "{0}";'.format(user_name)
            
        elif sel_user == '4':
            user_fist = input('Enter user first name: ')
            user_last = input('Enter user last name: ')
            #user_sql = 'SELECT first_name,last_name FROM %s WHERE name = %s' % (user_table, user_name)
            #cur.execute(user_sql)
            #data = cur.fetchall()
            #user = str(data).strip("(),")
            
            sql = 'SELECT user_id,first_name,last_name,checkout_date,address,equip_id FROM checked_out_items LEFT JOIN users ON checked_out_items.user_id = users.id WHERE users.first_name = "%s" AND users.last_name = "%s";' % (user_fist, user_last)
            
        db_select(sql)

    elif sel == '3':
        print('Check out item')
        first_name = input('first name: ')
        last_name = input('last name: ')
        eq_id = int(input('equipment id: '))
        check_avail_sql = 'SELECT available FROM %s WHERE id = "%d"' % (item_table, eq_id)
        check_avail(check_avail_sql)
        checkout_date = input('check out date(yyyy-mm-dd): ')
        return_by_date = input('return by date(yyyy-mm-dd): ')
        address = input('address: ')

        sql  = 'INSERT INTO %s (user_id) SELECT id FROM %s WHERE first_name = "%s" AND last_name = "%s";' % (chk_equip,user_table, first_name, last_name)
        if not return_by_date:
            sql1 = 'UPDATE %s SET equip_id = %d, address = "%s", checkout_date = "%s" WHERE id = LAST_INSERT_ID();' % (chk_equip,eq_id, address, checkout_date)            
        else:    
            sql1 = 'UPDATE %s SET equip_id = %d, address = "%s", checkout_date = "%s", return_date = "%s" WHERE id = LAST_INSERT_ID();' % (chk_equip, eq_id, address, checkout_date, return_by_date)
        
        avail_sql = 'UPDATE %s SET available = "no" WHERE id = %s;' % (item_table, eq_id)
        
        try:
            cur.execute(sql) 
            cur.execute(sql1)
            cur.execute(avail_sql)
            con.commit()
            print('succsess!')
       
        except mdb.Error as e:
            print('Failed to create record\nRolling back...')
            print("Error: %s" % e)
            con.rollback()


    elif sel == '4':                               # Check in returned items
        print('Check in Items')
        serial = input('s/n: ')
        returned = input('date returned(YYYY-MM-DD): ')
        """
        #check if item exist
        check = 'SELECT available FROM %S WHERE serial = "%s";' % item_table
        cur.execute(check)
        data = cur.fetchall()
        data = str(data).strip('()')
        
        if data == '':
            raise Exception('Item does not exist')
        """    
        sql = 'UPDATE %s SET available = "yes" WHERE serial = "%s";' % (item_table, serial)
        print('checking in item with serial: %s;' % serial)
        
        sql1 = 'UPDATE checked_out_items JOIN items ON checked_out_items.equip_id = items.id SET checked_out_items.date_returned = "%s" WHERE items.serial = "%s";' % (returned, serial)
        
        try:
            cur.execute(sql) 
            con.commit()
            print('succsess!')
              
        except mdb.Error as e:
            print('Failed to update record\nRolling back...')
            print("Error: %s" % e)
            con.rollback()
        
        try:    
            cur.execute(sql1)
            con.commit()
            print('succsess!')
       
        except mdb.Error as e:
            print('Failed to update record\nRolling back...')
            print("Error: %s" % e)
            con.rollback()
        
    elif sel == '5':                                # Add new items
        print('New Item Entry')
        sel = input('continue(yes/no): ')
        sel = sel.upper()
        if sel == 'Y' or sel == 'YES':
            loc = input('Enter location: ')
            room = input('Enter room: ')
            type = input('Enter item type: ')
            make = input('Enter make: ')
            model = input('Enter model: ')
            serial = input('Enter s/n: ')
            product = input('Enter product#: ')
            serv_tag = input('Enter service tag: ')
            os = input('Enter os: ')
            comp_name = input('Enter computer name: ')
            avail = input('Enter availability(YES/NO): ')
            notes = input('NOTES: ')
        
            long_str = [loc,room,type,make,model,serial,product,serv_tag,os,comp_name, \
                       avail,notes]

            for n,i in enumerate(long_str):
                if i == '':
                    long_str[n] = 'NULL'
        
            long_str = str(long_str).strip('[]').replace("'", '"')
            print(long_str)
        
            col_names = ['location','room','type','make','model','serial','product','service_tag','os', \
                        'computer_name', 'available','notes']
             
            col_names = str(col_names).strip('[]').replace("'", '')
        
        
            sql = 'INSERT INTO %s (%s) VALUES(%s)' % (col_names, item_table, long_str)
            print(sql)

            db_insert(sql)            
        else: 
            break
            
    elif sel == '6':
        print('Add User Entry')
        sel = input('Continue(yes/no): ')
        sel = sel.upper()
        if sel == 'Y' or sel == 'YES':
            first = input('Enter first name: ')
            last = input('Enter last name: ')
            email = input('Enter email address: ')
            
            long_str = [first,last,email]
            long_str = str(long_str).strip('[]').replace("'", '"')
            
            col_names = ['first_name','last_name','email']
            col_names = str(col_names).strip('[]').replace("'", '')
            
            sql = 'INSERT INTO %s (%s) VALUES(%s)' % (user_table,col_names,long_str)
            print(sql)

            db_insert(sql)
                      
        else:
            break
        
    
    elif sel == 'exit' or sel == 'quit' or sel == 'q':
        exit()
        
    else:
        print(unknown_sel)
        
con.close()

exit()