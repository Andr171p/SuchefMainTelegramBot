class OrdersSQL:
    create_table_query = "CREATE TABLE `users_orders`(id int AUTO_INCREMENT," \
                                 " phone_number varchar(32)," \
                                 " client longtext," \
                                 " number varchar(32)," \
                                 " date varchar(32)," \
                                 " status varchar(32)," \
                                 " sent int," \
                                 " amount int," \
                                 " pay_link longtext," \
                                 " pay_status varchar(32)," \
                                 " cooking_time_from varchar(32)," \
                                 " cooking_time_to varchar(32)," \
                                 " delivery_time_from varchar(32)," \
                                 " delivery_time_to varchar(32)," \
                                 " project varchar(32)," \
                                 " trade_point longtext," \
                                 " trade_point_card longtext," \
                                 " delivery_method varchar(32)," \
                                 " delivery_adress longtext, PRIMARY KEY (id));"
    drop_table_query = "DROP TABLE `users_orders`"
    clear_table_query = "TRUNCATE TABLE `users_orders`"
    select_all_data_query = "SELECT * FROM `users_orders`"
    insert_data_query = "INSERT INTO `users_orders`" \
                        "(phone_number, client, number, date, status, amount, pay_link, pay_status, cooking_time_from, cooking_time_to, delivery_time_from, delivery_time_to, project, trade_point, trade_point_card, delivery_method, delivery_adress)" \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_from_phone_number_query = "SELECT * FROM `users_orders` WHERE phone_number = %s"
    update_sent_query = " UPDATE `users_orders`" \
                        " SET sent=1" \
                        " WHERE status IN "
    check_sent_query = " SELECT *" \
                       " FROM `users_orders`" \
                       " WHERE phone_number=%s AND sent=1"
    get_order_query = " SELECT *" \
                      " FROM `users_orders`" \
                      " WHERE phone_number = %s AND number = %s"
    update_data_query = " UPDATE `users_orders`" \
                        " SET status = %s" \
                        " WHERE number = %s"
    delete_data_query = " DELETE FROM `users_orders`" \
                        " WHERE phone_number = %s"