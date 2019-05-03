#trabalhando com imagem para adicionar o logo da jatinox
#from reportlab.lib.utils import ImageReader
from reportlab.lib import utils
from reportlab.platypus import Image

from reportlab.lib.units import cm
class Logo(object):
	def __init__(seft, path, env):
		return 1

	#Obtem imagem já redimensionada.
	def get_image(path, width=1*cm):
		img = utils.ImageReader(path)
		iw, ih = img.getSize()
		aspect = ih / float(iw)
		return Image(path, width=width, height=(width * aspect))
