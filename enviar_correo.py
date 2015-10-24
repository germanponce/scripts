# importamos la libreria smtplib (no es necesario instalarlo)
import smtplib
# importamos librerias  para construir el mensaje
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#importamos librerias para adjuntar
from email.MIMEBase import MIMEBase
from email import encoders 

# definimos los correo de remitente y receptor
##se envia un mail a
addr_to   = 'luizmirodriguez@gmail.com'
##el mail sale desde el correo
addr_from = 'info@luisrodriguez.pe'

# Define SMTP email server details
smtp_server = 'mail.dominio.com.pe'
smtp_user   = 'lrodriguez@dominio.com.pe'
smtp_pass   = '**********'

# Construimos el mail
msg = MIMEMultipart()
msg['To'] = addr_to
msg['From'] = addr_from
msg['Subject'] = 'Prueba'
#cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
msg.attach(MIMEText('< h1>titulo de mensaje< p>cuerpo de mensaje','html'))

#adjuntamos fichero de texto pero puede ser cualquer tipo de archivo
##cargamos el archivo a adjuntar
fp = open('/tmp/log_envio.txt','rb')
adjunto = MIMEBase('multipart', 'encrypted')
#lo insertamos en una variable
adjunto.set_payload(fp.read())
fp.close()
#lo encriptamos en base64 para enviarlo
encoders.encode_base64(adjunto)
#agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
adjunto.add_header('Content-Disposition', 'attachment', filename='nombre_que_deseamos_que_tenga_el_adjunto.txt')
#adjuntamos al mensaje
msg.attach(adjunto) 

# inicializamos el stmp para hacer el envio
server = smtplib.SMTP(smtp_server)
server.starttls()
#logeamos con los datos ya seteamos en la parte superior
server.login(smtp_user,smtp_pass)
#el envio
server.sendmail(addr_from, addr_to, msg.as_string())
#apagamos conexion stmp
server.quit()
