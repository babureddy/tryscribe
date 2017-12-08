import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
#Next, log in to the server
server.login("babureddy1969@gmail.com", "babs331969")

#Send the mail
msg = "\r\n".join([
  "From: babureddy1969@gmail.com",
  "To: babureddy1969@gmail.com",
  "Subject: Just a message",
  "",
  "Why, oh why"
  ])
server.sendmail("babureddy1969@gmail.com", "babureddy1969@gmail.com", msg)
