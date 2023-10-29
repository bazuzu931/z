import os
from PIL import Image
import random
from rich.console import Console
cp = Console().print

min_duration = 1
max_duraion = 60

#---- Filter by duration ---------------------------------------------------------------------------------

def get_duration(filename):
	from moviepy.editor import VideoFileClip
	clip = VideoFileClip(filename)
	return int(clip.duration)

#---- Main ---------------------------------------------------------------------------------

def converting(post_path):
	for ffroot, dd, ff in os.walk(post_path):
		if ff:
			for f in ff:
				f = os.path.join(ffroot, f)
				if '.mp4' not in f:
					f = str(f)
					cp(f'[yellow]Converting .... {f}')
					new_name = 'a' + ''.join(random.choice('abcefgklmnporwzx123456789') for _ in range(7)) + '.jpg'
					try:
						im = Image.open(f)
						im.save(os.path.join(ffroot, new_name))
					except Exception as e:
						print('File is corrupted: ', f)
						print('File is deleting ... :', f)
						os.remove(os.path.abspath(f))
						pass
					os.remove(f)
					cp('[yellow]Convertation is Done!')
				else:
					f = str(f)
					cp(f'[yellow]Rename mp4 .... {f}')
					new_name = 'a' + ''.join(random.choice('abcefgklmnporwzx123456789') for _ in range(7)) + '.mp4'
					new_name = os.path.join(ffroot, new_name)
					if min_duration < get_duration(f) < max_duraion:
						os.rename(f, new_name)
						cp('[yellow]Rename of mp4 File is Done!')
					else:
						os.remove(f)
						cp('[red] Длительность видео не соответсвует. Видео удалено.')
