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


bl_info = {
    "name" : "GZ_MatchTransforms -- by AlbertoGZ",
    "author" : "AlbertoGZ",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}


import bpy

from .GZ_MatchTransforms import *



''''''''''''''''''''''''''''''''''''''''''''''''''''
    
            REGISTER AND UNREGISTER
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''

classes = (
    mainPanel,
    fromGetSelectedBtn,
    FROM_UL_List,
    fromGetSelectedClearListBtn,
    fromGetSelectedCollection,
    toGetSelectedBtn,
    TO_UL_List,
    toGetSelectedClearListBtn,
    toGetSelectedCollection,
    matchProperties,
    matchBtn,
    aboutBtn
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    # Custom scene properties
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=matchProperties)

    bpy.types.Scene.fromObjs = CollectionProperty(type=fromGetSelectedCollection)
    bpy.types.Scene.fromObjs_index = IntProperty()
    bpy.types.Scene.toObjs = CollectionProperty(type=toGetSelectedCollection)
    bpy.types.Scene.toObjs_index = IntProperty()


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
        
    del bpy.types.Scene.my_tool

    del bpy.types.Scene.fromObjs
    del bpy.types.Scene.fromObjs_index
    del bpy.types.Scene.toObjs
    del bpy.types.Scene.toObjs_index




if __name__ == "__main__":
    register()