# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

'''
GZ_MatchTransforms

Description: GZ_MatchTransforms (A.K.A matchMultiObject) 
makes match transformations on multiple objects by paired 
objects given a first selection list for the origin objects 
and second selection list to target objects.

Author: AlbertoGZ
albertogzonline@gmail.com
https://github.com/albertogz-dev

'''



import bpy

from bpy.props import(
                        BoolProperty,
                        PointerProperty,
                        StringProperty,
                        IntProperty,
                        CollectionProperty
)  

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       UIList
                       )




''''''''''''''''''''''''''''''''''''''''''''''''''''
    
                    UI PANEL
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''
class mainPanel(Panel):
    bl_label = "GZ_MatchTransforms -- by AlbertoGZ"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'GZ Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        row0 = layout.row()
        row0.alignment = 'RIGHT'
        row0.scale_y = 1
        row0.operator("object.about_btn")


        # Create two columns, by using a split layout.
        row1 = layout.split()

        # First column
        col1 = row1.column()
        col1.label(text="From: " + str(len(fromGetSelected)))
        col1.operator("object.from_get_select_btn")
        col1.operator("object.from_clear_list_btn")
        col1.template_list("FROM_UL_List", "", scene, "fromObjs", scene, "fromObjs_index", rows=4)
       
        # Second column
        col2 = row1.column()
        col2.label(text="To: " + str(len(toGetSelected)))
        col2.operator("object.to_get_select_btn")
        col2.operator("object.to_clear_list_btn")
        col2.template_list("TO_UL_List", "", scene, "toObjs", scene, "toObjs_index", rows=4)
      
        row2 = layout.row()
        row2.prop(mytool, "posChk", text="Position")
        row2.prop(mytool, "rotChk", text="Rotation")
        row2.prop(mytool, "sclChk", text="Scale")
 
        row3 = layout.row()
        row3.scale_y = 2.0
        row3.operator("object.match_btn")

       

   




''''''''''''''''''''''''''''''''''''''''''''''''''''
    
                    OPERATORS
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''


### 'FROM' SECTION
#
class fromGetSelectedBtn(Operator):
    bl_idname = "object.from_get_select_btn"
    bl_label = "Get Selected"
    bl_description = 'Get origin items to match transforms'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        fromGetSelectedFn(self)
        #getObjectSelection(self, context)
        return{'FINISHED'}
        
        
class FROM_UL_List(UIList):    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.obj
        custom_icon = "OUTLINER_OB_%s" % obj.type
        split = layout.split(factor=0.1)
        split.label(text=str(index))
        split.prop(obj, "name", text="", emboss=False, translate=False, icon=custom_icon)


class fromGetSelectedClearListBtn(Operator):
    # Clear all items of the list
    bl_idname = "object.from_clear_list_btn"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.fromObjs)

    #def invoke(self, context, event):
    #    return context.window_manager.invoke_confirm(self, event)
        
    def execute(self, context):
        global fromGetSelected
        fromGetSelectedClearListFn(self)      
        return{'FINISHED'}



### 'TO' SECTION
#
class toGetSelectedBtn(Operator):
    bl_idname = "object.to_get_select_btn"
    bl_label = "Get Selected"
    bl_description = 'Get target items to get match transforms'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        toGetSelectedFn(self)
        return{'FINISHED'}
        

class TO_UL_List(UIList):    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.obj
        custom_icon = "OUTLINER_OB_%s" % obj.type
        split = layout.split(factor=0.1)
        split.label(text=str(index))
        split.prop(obj, "name", text="", emboss=False, translate=False, icon=custom_icon)


class toGetSelectedClearListBtn(Operator):
    # Clear all items of the list
    bl_idname = "object.to_clear_list_btn"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.toObjs)

    #def invoke(self, context, event):
    #    return context.window_manager.invoke_confirm(self, event)
        
    def execute(self, context):
        global fromGetSelected
        toGetSelectedClearListFn(self)      
        return{'FINISHED'}


class aboutBtn(Operator):
    bl_idname = "object.about_btn"
    bl_label = "About"
    bl_description = ""

    @classmethod
    def poll(cls, context):
        return bool(True)

    def invoke(self, context, event):
        return showMessageBox('GZ_MatchTransforms v0.1.0', 'by AlbertoGZ', 'github.com / albertogz-dev', 'INFO')
        
    def execute(self, context):
       #      
        return{'FINISHED'}





''''''''''''''''''''''''''''''''''''''''''''''''''''
    
                    PROPERTIES
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''

class matchProperties(PropertyGroup):

    posChk : BoolProperty(
        name="Match position",
        description="Match position",
        default = True
        )

    rotChk : BoolProperty(
        name="Match rotation",
        description="Match rotation",
        default = True
        )

    sclChk : BoolProperty(
        name="Match scale",
        description="Match scale",
        default = True
        )
    

class matchBtn(Operator):
    bl_idname = "object.match_btn"
    bl_label = "Match Transforms"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        matchTransformsFn(self)
        return {'FINISHED'}








''''''''''''''''''''''''''''''''''''''''''''''''''''
    
                    FUNCTIONS
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''


global fromGetSelected
fromGetSelected = []

global toGetSelected
toGetSelected = []

global matchBtnStatus
matchBtnStatus = True


def fromGetSelectedFn(self):
    global fromGetSelected
    selection =  bpy.context.selected_objects
    fromGetSelected = []
    fromGetSelectedClearListFn(self)
    for obj in selection:
        item = bpy.context.scene.fromObjs.add()
        item.name = obj.name
        item.obj = obj
        fromGetSelected.append(obj.name)
    #print(fromGetSelected)
    return{'FINISHED'}


def fromGetSelectedClearListFn(self):
    global fromGetSelected
    fromGetSelected = []
    bpy.context.scene.fromObjs.clear()
    return{'FINISHED'}



def toGetSelectedFn(self):
    global toGetSelected
    selection =  bpy.context.selected_objects
    toGetSelected = []
    toGetSelectedClearListFn(self)
    for obj in selection:
        item = bpy.context.scene.toObjs.add()
        item.name = obj.name
        item.obj = obj
        toGetSelected.append(obj.name)
    #print(toGetSelected)
    return{'FINISHED'}


def toGetSelectedClearListFn(self):
    global toGetSelected
    toGetSelected = []
    bpy.context.scene.toObjs.clear()
    return{'FINISHED'}



def matchTransformsFn(self):
    mytool = bpy.context.scene.my_tool
    try:
        fromGetSelected or toGetSelected
        if len(fromGetSelected) < 1 or len(toGetSelected) < 1:
            self.report({'INFO'}, 'Must be selected at least one item in both lists.')
            showMessageBox('', 'Must be selected at least one item in both lists.', '', 'INFO')

        if (mytool.posChk == False) and (mytool.rotChk == False) and (mytool.sclChk == False):
            self.report({'INFO'}, 'Must be checked at least one transform property.')
            showMessageBox('', 'Must be checked at least one transform property.', '', 'INFO')
        
        else:   
            for f, t, in zip(fromGetSelected, toGetSelected):
                if (mytool.posChk == True):
                    bpy.context.scene.objects[f].location = bpy.context.scene.objects[t].location
                
                if (mytool.rotChk == True):
                    bpy.context.scene.objects[f].rotation_euler = bpy.context.scene.objects[t].rotation_euler

                if (mytool.sclChk == True):    
                    bpy.context.scene.objects[f].scale = bpy.context.scene.objects[t].scale
            
                self.report({'INFO'}, (str(len(fromGetSelected)) + ' items successfully matched!'))
                showMessageBox('', '' + str(len(fromGetSelected)) + ' items successfully matched!', '', 'INFO')
                
            fromGetSelectedClearListFn(self)
            toGetSelectedClearListFn(self)
    except NameError:
        print("none")
    
    return{'FINISHED'}



def showMessageBox(msg="", msg1="", msg2="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=msg)
        self.layout.label(text=msg1)
        self.layout.label(text=msg2)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
    
    return{'FINISHED'}







''''''''''''''''''''''''''''''''''''''''''''''''''''
    
                   COLLECTIONS
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''

class fromGetSelectedCollection(PropertyGroup):
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)                   
            

class toGetSelectedCollection(PropertyGroup):
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)
    