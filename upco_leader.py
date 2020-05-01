from PIL import Image, ImageColor, ImageDraw, ImageFont
import math, sys, pathlib



def drawLinearRamp(width=500, height=25, file_output=None):

	image = Image.new("RGBA", (width, height), (128,128,128,0))
	draw_image= ImageDraw.Draw(image)

	for x in range(width):
		hsv = ImageColor.getrgb(f"hsv(0, 0%, {x/width*100}%)")
		draw_image.line([(x, 0), (x,height-1)], width=1, fill=hsv)

	if file_output:
		image.save(file_output)
	else:
		return image

def drawColorRamp(width=500, height=25, file_output=None):

	image = Image.new("RGBA", (width,height), (128,128,128,0))
	draw_image = ImageDraw.Draw(image)

	for x in range(width):
		hue = x/width * 360
		hsv = ImageColor.getrgb(f"hsv({hue},100%,100%)")
		draw_image.line([(x, 0), (x, height-1)], width=1, fill=hsv)

	if file_output:
		image.save(file_output)
	else:
		return image



def drawCountdown(radius=800, seconds=8, frame=0, framerate=24, no_twopop=False, file_output=None):

	supersample = 4
	radius *= supersample

	image = Image.new("RGBA", (radius*2, radius*2), (128,128,128,0))

	if no_twopop==False and frame > (seconds-2)*framerate:
		if file_output:
			image.save(file_output)
			return file_output
		else:
			return image
	
	# Decide if this is the twopop frame or not
	is_twopop = no_twopop==False and frame == (seconds-2)*framerate

	draw_image = ImageDraw.Draw(image)

	# Draw the clock circles ======
	circle_stroke_width = 10 * supersample
	circle_inner_offset = 4 * circle_stroke_width  # 2 leaves an empty area the side of the stroke width between the two circles

	# Countdown pie fill
	draw_image.pieslice(
		xy=[(0,0),(radius*2, radius*2)],
		start=270,
		end=270 + (frame%framerate/framerate * 360),
		fill=(255,255,255,128)
	)

	# Outer circle stroke
	draw_image.ellipse(
		xy=[(0,0),(radius*2, radius*2)],
		fill=None if not is_twopop else (255,255,255,255),	# White if 2pop frame
		outline=(0,0,0,255),
		width=circle_stroke_width
	)

	# Inner circle stroke
	draw_image.ellipse(
		xy=[(0+circle_inner_offset),(0+circle_inner_offset), (radius* 2 - circle_inner_offset), (radius*2 - circle_inner_offset)],
		fill=None if not is_twopop else (255,255,255,255),	# White if 2pop frame
		outline=(0,0,0,255),
		width=circle_stroke_width
	)


	# Draw the count
	count_text = str(seconds - frame // framerate)

	text_font = ImageFont.truetype("arialbd.ttf", size=int(1.25 * radius))
	text_offset = draw_image.textsize(count_text, font=text_font)	# TODO: textsize() seems to be incorrect -- using 1.65 Y offset for correction
	print(f"Using {text_offset}")
	draw_image.text(
		xy=[(radius - int(text_offset[0]/2)) - int(circle_stroke_width/2), (radius - int(text_offset[1]/1.65) - int(circle_stroke_width/2))],
		text=count_text,
		fill=(0,0,0,255),
		stroke_width=circle_stroke_width,
		stroke_fill=(255,255,255,255),
		font=text_font
	)

	image = image.resize((int(radius*2/supersample), int(radius*2/supersample)), Image.BOX)
	
	if file_output:
		image.save(file_output)
	else:
		return image

def drawStar(spokes=128, radius=200, file_output=None):

	# Supersample
	radius *= 4

	color_dark  = (0,0,0,255)
	color_light = (255,255,255,255)

	image = Image.new("RGBA", (radius*2, radius*2), (128,128,128,0))

	draw_star = ImageDraw.Draw(image)

	spoke_angle = 360/spokes
	spoke_angle_offset = spoke_angle/2

	for x in range(spokes):
		if x%2: color_spoke = color_light
		else:   color_spoke = color_dark
		draw_star.pieslice([(2,2),(radius*2-2, radius*2-2)], (spoke_angle*x)-spoke_angle_offset, (spoke_angle*(x+1))-spoke_angle_offset, fill=color_spoke)

	image = image.resize((int(radius/2), int(radius/2)), Image.BOX)
	
	if file_output:
		image.save(file_output)
	else:
		return image

def drawFrameOverlay(frame_width=2160, frame_height=1080, active_width=2048, active_height=858, offset_x=0, offset_y=0, file_output=None):

	# Arrow dimensions
	# Recommend even numbers for symmetry
	arrow_base = 24
	arrow_height = 30

	# Colors
	# RGBA Values
	color_dark_transparent 	= (0,0,0,128)
	color_light_transparent = (255,255,255,128)

	# Font properties
	text_font = ImageFont.truetype("arialbd.ttf", size=16)
	text_offset = 5  # Pixel offset from reticle edge



	image = Image.new("RGBA", (frame_width, frame_height), ImageColor.getrgb("rgba(0,0,0,0)"))


	# Calculate useful pixel coordinates
	coord_frm_middle = (int(frame_width/2), int(frame_height/2))
	coord_ret_start = (int((frame_width - active_width)/2) + offset_x, int((frame_height - active_height) / 2) + offset_y)
	coord_ret_end   = (coord_ret_start[0] + active_width, coord_ret_start[1] + active_height)

	# Prepare drawing context
	draw_reticle = ImageDraw.Draw(image)

	draw_reticle.rectangle([(0,0),(frame_width, frame_height)], fill=color_dark_transparent)


	# Draw reticle =============
	draw_reticle.rectangle([coord_ret_start, coord_ret_end], outline=color_light_transparent, fill=(255,255,255,0), width=3)

	# Draw crosshairs
	draw_reticle.line([int(frame_width/2), coord_ret_start[1], int(frame_width/2), coord_ret_end[1]], fill=color_light_transparent, width=1)
	draw_reticle.line([coord_ret_start[0], int(frame_height/2), coord_ret_end[0], int(frame_height/2)], fill=color_light_transparent, width=1)


	# Draw arrows ==============

	# Top Arrow
	draw_reticle.polygon([
		(coord_frm_middle[0], coord_ret_start[1]),  # Top middle
		(coord_frm_middle[0] + arrow_base/2, coord_ret_start[1] + arrow_height),
		(coord_frm_middle[0] - arrow_base/2, coord_ret_start[1] + arrow_height)
	], fill=(255,255,255,128))

	# Bottom Arrow
	draw_reticle.polygon([
		(coord_frm_middle[0], coord_ret_end[1]),  # Bottom middle
		(coord_frm_middle[0] + arrow_base/2, coord_ret_end[1] - arrow_height),
		(coord_frm_middle[0] - arrow_base/2, coord_ret_end[1] - arrow_height)
	], fill=(255,255,255,128))

	# Left Arrow
	draw_reticle.polygon([
		(coord_ret_start[0], coord_frm_middle[1]),  # Left middle
		(coord_ret_start[0] + arrow_height, coord_frm_middle[1] + arrow_base/2),
		(coord_ret_start[0] + arrow_height, coord_frm_middle[1] - arrow_base/2)
	], fill=(255,255,255,128))

	# Right Arrow
	draw_reticle.polygon([
		(coord_ret_end[0], coord_frm_middle[1]),  # Right middle
		(coord_ret_end[0] - arrow_height, coord_frm_middle[1] + arrow_base/2),
		(coord_ret_end[0] - arrow_height, coord_frm_middle[1] - arrow_base/2)
	], fill=(255,255,255,128))


	# Shade outside reticle
	# EDIT: Taken care of before drawing other stuff
	#draw_reticle.rectangle([(0,0),(frame_width, coord_ret_start[1])], fill=color_dark_transparent)									# Top
	#draw_reticle.rectangle([(0,coord_ret_end[1]),(frame_width, frame_height)], fill=color_dark_transparent)						# Bottom
	#draw_reticle.rectangle([(0,coord_ret_start[1]),(coord_ret_start[0], coord_ret_end[1])], fill=color_dark_transparent)			# Left
	#draw_reticle.rectangle([(coord_ret_end[0],coord_ret_start[1]),(frame_width, coord_ret_end[1])], fill=color_dark_transparent)	# Right


	# Print framing info
	text_framing = f"{(active_width/active_height):.2f} ASPECT RATIO ({active_width}x{active_height})"
	text_framing_width, text_framing_height = draw_reticle.textsize(text_framing, font=text_font)

	coord_text_uni = (coord_ret_start[0], coord_ret_end[1] + text_offset)
	coord_text_asp = (coord_ret_end[0] - text_framing_width, coord_ret_end[1] + text_offset)
	color_text = color_light_transparent

	# If text won't fit between reticle and edge of frame, put it inside
	if coord_text_asp[1] + text_framing_height > frame_height:
		coord_text_uni = (coord_ret_start[0] + text_offset, coord_ret_end[1] - text_framing_height - text_offset)
		coord_text_asp = (coord_ret_end[0] - text_framing_width - text_offset, coord_ret_end[1] - text_framing_height - text_offset)
		color_text = color_dark_transparent

	draw_reticle.text(coord_text_uni,
		"UNIVERSAL PICTURES",
		font=text_font,
		fill=color_text,
		align="left"
	)

	draw_reticle.text(coord_text_asp,
		text_framing,
		font=text_font,
		fill=color_text,
		align="right")


	if file_output:
		image.save(file_output)
	
	else:
		return image


if __name__ == "__main__":

	seconds = 8
	framerate = 24
	framecount = seconds * framerate

	out_path = pathlib.Path(sys.argv[-1])
	
	for x in range(framecount):
		frame_path = pathlib.Path(out_path.parent, out_path.stem + '_' + str(x).zfill(8) + out_path.suffix)
		drawCountdown(file_output=frame_path, seconds=seconds, framerate=framerate, frame=x)