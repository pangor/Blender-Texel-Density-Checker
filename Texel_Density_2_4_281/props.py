import bpy

from bpy.props import (
		StringProperty,
		EnumProperty,
        BoolProperty,
        PointerProperty,
        )

from . import viz_operators

def Change_Texture_Size(self, context):
	td = context.scene.td
	
	#Check exist texture image
	flag_exist_texture = False
	for t in range(len(bpy.data.images)):
		if bpy.data.images[t].name == 'TD_Checker':
			flag_exist_texture = True
				
	checker_rexolution_x = 1024
	checker_rexolution_y = 1024
	
	#Get texture size from panel
	if td.texture_size == '0':
		checker_rexolution_x = 512
		checker_rexolution_y = 512
	if td.texture_size == '1':
		checker_rexolution_x = 1024
		checker_rexolution_y = 1024
	if td.texture_size == '2':
		checker_rexolution_x = 2048
		checker_rexolution_y = 2048
	if td.texture_size == '3':
		checker_rexolution_x = 4096
		checker_rexolution_y = 4096
	if td.texture_size == '4':
		try:
			checker_rexolution_x = int(td.custom_width)
		except:
			checker_rexolution_x = 1024
			td['custom_width'] = '1024'
			
		try:
			checker_rexolution_y = int(td.custom_height)
		except:
			checker_rexolution_y = 1024
			td['custom_height'] = '1024'

	if checker_rexolution_x < 1 or checker_rexolution_y < 1:
		checker_rexolution_x = 1024
		checker_rexolution_y = 1024
		td['custom_width'] = '1024'
		td['custom_height'] = '1024'

	if flag_exist_texture:
		bpy.data.images['TD_Checker'].generated_width = checker_rexolution_x
		bpy.data.images['TD_Checker'].generated_height = checker_rexolution_y
		bpy.data.images['TD_Checker'].generated_type=td.checker_type

	bpy.ops.object.texel_density_check()


def Change_Units(self, context):
	td = context.scene.td
	bpy.ops.object.texel_density_check()


def Change_Texture_Type(self, context):
	td = context.scene.td
	
	#Check exist texture image
	flag_exist_texture = False
	for t in range(len(bpy.data.images)):
		if bpy.data.images[t].name == 'TD_Checker':
			flag_exist_texture = True
			
	if flag_exist_texture:
		bpy.data.images['TD_Checker'].generated_type=td.checker_type


def Filter_Bake_VC_Min_TD(self, context):
	td = context.scene.td
	bake_vc_min_td_filtered = td['bake_vc_min_td'].replace(',', '.')
	
	try:
		bake_vc_min_td = float(bake_vc_min_td_filtered)
	except:
		bake_vc_min_td = 0.01

	if (bake_vc_min_td<0.01):
		bake_vc_min_td = 0.01

	td['bake_vc_min_td'] = str(bake_vc_min_td)
	bpy.ops.object.bake_td_uv_to_vc()


def Filter_Bake_VC_Max_TD(self, context):
	td = context.scene.td
	bake_vc_max_td_filtered = td['bake_vc_max_td'].replace(',', '.')
	
	try:
		bake_vc_max_td = float(bake_vc_max_td_filtered)
	except:
		bake_vc_max_td = 0.01

	if (bake_vc_max_td<0.01):
		bake_vc_max_td = 0.01

	td['bake_vc_max_td'] = str(bake_vc_max_td)	
	bpy.ops.object.bake_td_uv_to_vc()


def Filter_Bake_VC_Min_Space(self, context):
	td = context.scene.td
	bake_vc_min_space_filtered = td['bake_vc_min_space'].replace(',', '.')
	
	try:
		bake_vc_min_space = float(bake_vc_min_space_filtered)
	except:
		bake_vc_min_space = 0.0001

	if (bake_vc_min_space<0.00001):
		bake_vc_min_space = 0.00001

	td['bake_vc_min_space'] = str(bake_vc_min_space)	
	bpy.ops.object.bake_td_uv_to_vc()


def Filter_Bake_VC_Max_Space(self, context):
	td = context.scene.td
	bake_vc_max_space_filtered = td['bake_vc_max_space'].replace(',', '.')
	
	try:
		bake_vc_max_space = float(bake_vc_max_space_filtered)
	except:
		bake_vc_max_space = 0.0001

	if (bake_vc_max_space<0.00001):
		bake_vc_max_space = 0.00001

	td['bake_vc_max_space'] = str(bake_vc_max_space)	
	bpy.ops.object.bake_td_uv_to_vc()


def Filter_Density_Set(self, context):
	td = context.scene.td
	density_set_filtered = td['density_set'].replace(',', '.')
	
	try:
		density_set = float(density_set_filtered)
	except:
		density_set = 2.0

	if (density_set<0.001):
		density_set = 0.001

	td['density_set'] = str(density_set)


def Change_Bake_VC_Mode(self, context):
	td = context.scene.td

	if td.bake_vc_mode == "TD_FACES_TO_VC" or td.bake_vc_mode == "TD_ISLANDS_TO_VC" or td.bake_vc_mode == "UV_SPACE_TO_VC":
		Show_Gradient(self, context)
	else:
		bpy.types.SpaceView3D.draw_handler_remove(draw_info["handler"], 'WINDOW')
		draw_info["handler"] = None

	bpy.ops.object.bake_td_uv_to_vc()

draw_info = {
	"handler": None,
}


def Show_Gradient(self, context):
	td = context.scene.td
	if td.bake_vc_show_gradient and draw_info["handler"] == None:
			draw_info["handler"] = bpy.types.SpaceView3D.draw_handler_add(viz_operators.Draw_Callback_Px, (None, None), 'WINDOW', 'POST_PIXEL')
	elif (not td.bake_vc_show_gradient) and (draw_info["handler"] != None):
		bpy.types.SpaceView3D.draw_handler_remove(draw_info["handler"], 'WINDOW')
		draw_info["handler"] = None


class TD_Addon_Props(bpy.types.PropertyGroup):
	uv_space: StringProperty(
		name="",
		description="wasting of uv space",
		default="0 %")
	
	density: StringProperty(
		name="",
		description="Texel Density",
		default="0")
	
	density_set: StringProperty(
		name="",
		description="Texel Density",
		default="0",
		update = Filter_Density_Set)
	
	tex_size = (('0','512px',''),('1','1024px',''),('2','2048px',''),('3','4096px',''), ('4','Custom',''))
	texture_size: EnumProperty(name="", items = tex_size, update = Change_Texture_Size)
	
	selected_faces: BoolProperty(
		name="Selected Faces",
		description="Operate only on selected faces",
		default = True)
	
	custom_width: StringProperty(
		name="",
		description="Custom Width",
		default="1024",
		update = Change_Texture_Size)
	
	custom_height: StringProperty(
		name="",
		description="Custom Height",
		default="1024",
		update = Change_Texture_Size)
	
	units_list = (('0','px/cm',''),('1','px/m',''), ('2','px/in',''), ('3','px/ft',''))
	units: EnumProperty(name="", items = units_list, update = Change_Units)
	
	select_value: StringProperty(
		name="",
		description="Select Value",
		default="1.0")

	select_td_threshold: StringProperty(
		name="",
		description="Select Threshold",
		default="0.1")
	
	set_method_list = (('0','Each',''),('1','Average',''))
	set_method: EnumProperty(name="", items = set_method_list)

	checker_method_list = (('0','Replace',''), ('1','Store and Replace',''))
	checker_method: EnumProperty(name="", items = checker_method_list)

	checker_type_list = (('COLOR_GRID','Color Grid',''),('UV_GRID','UV Grid',''))
	checker_type: EnumProperty(name="", items = checker_type_list, update = Change_Texture_Type)

	bake_vc_min_td: StringProperty(
		name="",
		description="Min TD",
		default="0.64",
		update = Filter_Bake_VC_Min_TD)

	bake_vc_max_td: StringProperty(
		name="",
		description="Max TD",
		default="10.24",
		update = Filter_Bake_VC_Max_TD)

	bake_vc_show_gradient: BoolProperty(
		name="Show Gradient",
		description="Show Gradient in Viewport",
		default = False,
		update = Show_Gradient)

	bake_vc_mode_list = (('TD_FACES_TO_VC','Texel (By Face)',''), ('TD_ISLANDS_TO_VC','Texel (By Island)',''),('UV_ISLANDS_TO_VC','UV Islands',''), ('UV_SPACE_TO_VC','UV Space (%)',''))
	bake_vc_mode: EnumProperty(name="", items = bake_vc_mode_list, update = Change_Bake_VC_Mode)

	bake_vc_min_space: StringProperty(
		name="",
		description="Min UV Space",
		default="0.0001",
		update = Filter_Bake_VC_Min_Space)

	bake_vc_max_space: StringProperty(
		name="",
		description="Max UV Space",
		default="2.0",
		update = Filter_Bake_VC_Max_Space)

	select_mode_list = (('FACES_BY_TD','Faces (By Texel)',''), ('ISLANDS_BY_TD','Islands (By Texel)',''), ('ISLANDS_BY_SPACE','Islands (By UV Space)',''))
	select_mode: EnumProperty(name="", items = select_mode_list)


classes = (
	TD_Addon_Props,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.td = PointerProperty(type=TD_Addon_Props)


def unregister():
	if draw_info["handler"] != None:
		bpy.types.SpaceView3D.draw_handler_remove(draw_info["handler"], 'WINDOW')
		draw_info["handler"] = None

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.td