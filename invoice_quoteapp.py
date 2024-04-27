# let's create an app that will create a quote and invoice with automatic sending to the customer's email address
# it should work on mobile and desktop
# it should be able to create a quote and invoice as a pdf file
# it should be able to send the quote and invoice to the customer's email address

# import the necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from fpdf import FPDF
from PIL import Image
from io import BytesIO

# create a connection to the database
def create_connection():
    conn = sqlite3.connect("invoice_quote.db")
    return conn

# create the tables in the database
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, customer_email TEXT, quote_data TEXT, created_at TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_email TEXT, invoice_data TEXT, created_at TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, customer_email TEXT, reminder_data TEXT, created_at TIMESTAMP)''')
    conn.commit()

# save the data to the database
def save_data(conn, table, data):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table} (customer_email, {table[:-1]}_data, created_at) VALUES (?, ?, ?)", (data['customer_email'], data[f'{table[:-1]}_data'], datetime.now()))
    conn.commit()

# send the email to the customer
def send_email(receiver_email, subject, body):
    sender_email = os.environ['EMAIL_ADDRESS']
    password = os.environ['EMAIL_PASSWORD']

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# create the quote
def create_quote(customer_email, quote_data):
    conn = create_connection()
    save_data(conn, 'quotes', {'customer_email': customer_email, 'quote_data': quote_data})
    send_email(customer_email, "Your Quote", quote_data)
    conn.close()

# create the invoice
def create_invoice(customer_email, invoice_data):
    conn = create_connection()
    save_data(conn, 'invoices', {'customer_email': customer_email, 'invoice_data': invoice_data})
    send_email(customer_email, "Your Invoice", invoice_data)
    conn.close()

# send the reminder
def send_reminder(customer_email, reminder_data):
    conn = create_connection()
    save_data(conn, 'reminders', {'customer_email': customer_email, 'reminder_data': reminder_data})
    send_email(customer_email, "Payment Reminder", reminder_data)
    conn.close()

# create the pdf file
def create_pdf_file(data, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output(file_name, 'F')

# create the app
def main():
    # create the connection to the database
    conn = create_connection()
    # create the tables in the database
    create_tables(conn)

    # create the sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Home", "Quote", "Invoice", "Reminder"])
    if app_mode == "Home":
        st.title("Welcome to the Invoice and Quote App")
        st.write("This app will help you create quotes and invoices for your customers. It will also send the quotes and invoices to your customers.")
        st.write("Please choose the app mode from the sidebar to create a quote or invoice.")
    elif app_mode == "Quote":
        st.title("Create a Quote")
        st.write("Please enter the details below to create a quote.")
        customer_email = st.text_input("Enter the customer's email address")
        quote_data = st.text_area("Enter the quote details")
        if st.button("Create Quote"):
            create_quote(customer_email, quote_data)
            st.success("Quote created successfully!")
    elif app_mode == "Invoice":
        st.title("Create an Invoice")
        st.write("Please enter the details below to create an invoice.")
        customer_email = st.text_input("Enter the customer's email address")
        invoice_data = st.text_area("Enter the invoice details")
        if st.button("Create Invoice"):
            create_invoice(customer_email, invoice_data)
            st.success("Invoice created successfully!")
    elif app_mode == "Reminder":
        st.title("Send a Reminder")
        st.write("Please enter the details below to send a reminder.")
        customer_email = st.text_input("Enter the customer's email address")
        reminder_data = st.text_area("Enter the reminder details")
        if st.button("Send Reminder"):
            send_reminder(customer_email, reminder_data)
            st.success("Reminder sent successfully!")

    # close the connection to the database
    conn.close()

if __name__ == "__main__":
    main()

# run the app
# streamlit run invoice_quoteapp.py








