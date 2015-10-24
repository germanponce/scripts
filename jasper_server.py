import os
import glob
import subprocess

path = "/home/german/openerp/70/cegasa_addons/jasper_reports/JasperReports"
env = {}
env.update( os.environ )
if os.name == 'nt':
    sep = ';'
else:
    sep = ':'
libs = os.path.join( path, '..', 'java', 'lib', '*.jar' )
env['CLASSPATH'] = os.path.join( path, '..', 'java' + sep ) + sep.join( glob.glob( libs ) ) + sep + os.path.join( path, '..', 'custom_reports' )
cwd = os.path.join( path, '..', 'java' )

# Set headless = True because otherwise, java may use existing X session and if session is
# closed JasperServer would start throwing exceptions. So we better avoid using the session at all.
command = ['java', '-Djava.awt.headless=true', '-Xms512M', '-Xmx1024M','com.nantic.jasperreports.JasperServer', unicode("8090")]
process = subprocess.Popen(command, env=env, cwd=cwd)
#if self.pidfile:
#    f = open( self.pidfile, 'w')
#    try:
#        f.write( str( process.pid ) )
#    finally:
#        f.close()


