import os

import bpy
from bpy_extras.io_utils import ImportHelper

from .utils.util import drawMultilineLabel, getPreferences
from .consts import ADDON_NAME

class DirectoryProperty(bpy.types.PropertyGroup):
    directory: bpy.props.StringProperty(name="", subtype='DIR_PATH')

class SelectDirectory(bpy.types.Operator, ImportHelper):
    """Select Directory"""
    bl_idname = "n2b.select_asset_dir"
    bl_label = "Select Directory"
    filename_ext = ""
    dirpath : bpy.props.StringProperty(name = "", description="Choose directory:", subtype='DIR_PATH')

    def execute(self, context):
        directory = os.path.dirname(self.filepath)
        newDir = getPreferences().assetDirs.add()
        newDir.directory = directory

        return {'FINISHED'}

class RemoveDirectory(bpy.types.Operator):
    """Remove Directory"""
    bl_idname = "n2b.remove_asset_dir"
    bl_label = "Remove Directory"

    index : bpy.props.IntProperty()

    def execute(self, context):
        getPreferences().assetDirs.remove(self.index)
        return {'FINISHED'}

ArmatureDisplayTypeEnum = [
    ("DEFAULT", "Default", ""),
    ("OCTAHEDRAL", "Octahedral", ""),
    ("STICK", "Stick", ""),
    ("BBONE", "B-Bone", ""),
    ("ENVELOPE", "Envelope", ""),
    ("WIRE", "Wire", "")
]

class N2B2NPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME
    assetDirs: bpy.props.CollectionProperty(type=DirectoryProperty)
    armatureDefaultDisplayType: bpy.props.EnumProperty(name="Armature Display Type", items=ArmatureDisplayTypeEnum, default="DEFAULT")
    armatureDefaultInFront: bpy.props.BoolProperty(name="Armature Default In Front", default=False)

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout

        box = layout.box()
        box.label(text="Default Armature Viewport Display Options:")
        row = box.row()
        row.label(text="Display Type:")
        row.prop(self, "armatureDefaultDisplayType", text="")
        row = box.row()
        row.label(text="In Front:")
        row.prop(self, "armatureDefaultInFront", text="")

        box = layout.box()
        drawMultilineLabel(context, "Assign extracted cpk directories below if you wish to enable bounding box visualization with layout import", box)
        for i, assetDir in enumerate(self.assetDirs):
            row = box.row(align=True)
            row.prop(self.assetDirs[i], "directory", text="")
            row.operator(RemoveDirectory.bl_idname, text="", icon="X").index = i
        box.operator(SelectDirectory.bl_idname, text="Add Directory", icon="FILE_FOLDER")

def register():
    bpy.utils.register_class(DirectoryProperty)
    bpy.utils.register_class(SelectDirectory)
    bpy.utils.register_class(RemoveDirectory)
    bpy.utils.register_class(N2B2NPreferences)

def unregister():
    bpy.utils.unregister_class(DirectoryProperty)
    bpy.utils.unregister_class(SelectDirectory)
    bpy.utils.unregister_class(RemoveDirectory)
    bpy.utils.unregister_class(N2B2NPreferences)
