# tkit v1.0 sep 8 2011 Several functions to select neighboring elements in a topology.
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name" : "Topokit",
    "author" : "Shams Kitz / dustractor@gmail.com",
    "version" : (1, 0),
    "blender" : (2, 5, 9),
    "api" : 39355,
    "location" : "View3d > Edit Mesh Specials (W key) > topokit",
    "description" : "Variouf wayf to felect neighboring elementf.",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "github.com/dustractor/tkit",
    "category" : "Mesh"
}
import bpy


def true(x):
    x.select = True

@property
def eki(mesh):
    return {e.key:e.index for e in mesh.edges}

@eki.setter
def eki(mesh,x):
    raise AttributeError

@property
def vsel(mesh):
    return {v.index for v in mesh.vertices if v.select}

@vsel.setter
def vsel(mesh,L):
    list(map(true,map(lambda i:mesh.vertices[i],L)))

@property
def esel(mesh):
    return {e.index for e in mesh.edges if e.select}

@esel.setter
def esel(mesh,L):
    list(map(true,map(lambda i:mesh.edges[i],L)))

@property
def fsel(mesh):
    return {f.index for f in mesh.faces if f.select}

@fsel.setter
def fsel(mesh,L):
    list(map(true,map(lambda i:mesh.faces[i],L)))

@property
def vv(mesh):
    d = {i:set() for i in range(len(mesh.vertices))}
    for v1,v2 in mesh.edge_keys:
        d[v1].add(v2)
        d[v2].add(v1)
    return d

@vv.setter
def vv(mesh,L):
    raise AttributeError

@property
def ve(mesh):
    d = {i:set() for i in range(len(mesh.vertices))}
    for e in mesh.edges:
        for v in e.vertices:
            d[v].add(e.index)
    return d

@ve.setter
def ve(mesh,L):
    raise AttributeError

@property
def vf(mesh):
    d={i:set() for i in range(len(mesh.vertices))}
    for f in mesh.faces:
        for v in f.vertices:
            d[v].add(f.index)
    return d

@vf.setter
def vf(mesh,L):
    raise AttributeError

@property
def ee(mesh):
    eki = mesh.eki
    d={i:set() for i in range(len(mesh.edges))}
    for f in mesh.faces:
        ed=[eki[ek] for ek in f.edge_keys]
        for k in f.edge_keys:
            d[eki[k]].update(ed)
    return d

@ee.setter
def ee(mesh,L):
    raise AttributeError

@property
def ef(mesh):
    eki = mesh.eki
    d = {i:set() for i in range(len(mesh.edges))}
    for f in mesh.faces:
        for k in f.edge_keys:
            d[eki[k]].add(f.index)
    return d

@ef.setter
def ef(mesh,L):
    raise AttributeError

@property
def ff(mesh):
    eki=mesh.eki
    ef=mesh.ef
    d={i:set() for i in range(len(mesh.faces))}
    for f in mesh.faces:
        for ek in f.edge_keys:
            d[f.index].update(ef[eki[ek]])
    return d

@ff.setter
def ff(mesh,L):
    raise AttributeError

@property
def svv(mesh):
    n=set()
    s=mesh.vsel
    m=mesh.vv
    d=filter(lambda x:x in s,m)
    for v in d:
        n.update(m[v])
    return n-s
@svv.setter
def svv(mesh,L):
    raise AttributeError

@property
def see(mesh):
    n=set()
    s=mesh.esel
    m=mesh.ee
    d=filter(lambda x:x in s,m)
    for e in d:
        n.update(m[e])
    return n-s
@see.setter
def see(mesh,L):
    raise AttributeError

@property
def sff(mesh):
    n=set()
    s=mesh.fsel
    m=mesh.ff
    d=filter(lambda x:x in s,m)
    for f in d:
        n.update(m[f])
    return n-s
@sff.setter
def sff(mesh,L):
    raise AttributeError

@property
def je(mesh):
    eki=mesh.eki
    fs=mesh.fsel
    es={i:0 for i in mesh.esel}
    for f in fs:
        for k in mesh.faces[f].edge_keys:
            es[eki[k]]+=1
    return list(filter(lambda x:es[x]<1,es))
@je.setter
def je(mesh,L):
    raise AttributeError

@property
def jei(mesh):
    es=mesh.esel
    a={i:False for i in es}
    z=set()
    ef=mesh.ef
    for e in es:
        for f in ef[e]:
            if mesh.faces[f].select:
                if not a[e]:
                    a[e]=True
                else:
                    z.add(e)
    for e in a:
        if a[e]:
            es.remove(e)
    es.update(z)
    return es
@jei.setter
def jei(mesh,L):
    raise AttributeError

@property
def e_lat(mesh):
    ts=set()
    eki=mesh.eki
    es=mesh.esel
    ef=mesh.ef
    for e in es:
        for f in ef[e]:
            for k in mesh.faces[f].edge_keys:
                vin=False
                for v in mesh.edges[e].key:
                    if v in k:
                        vin = True
                if vin:
                    continue
                else:
                    ts.add(eki[k])
    if ts.issubset(es):
        return []
    return ts-es
@e_lat.setter
def e_lat(mesh,L):
    raise AttributeError

@property
def e_lon(mesh):
    ts=set()
    ef=mesh.ef
    vv=mesh.vv
    ve=mesh.ve
    es=mesh.esel
    pts={}
    for v in mesh.vsel:
        pts[v]=False
    impfs=set()
    for e in es:
        for v in mesh.edges[e].key:
            pts[v] = not pts[v]
        for f in ef[e]:
            impfs.add(f)
    evs=[pt for pt in pts if pts[pt] == True]
    implicated_face_verts=set()
    epneighbors=set()
    for f in impfs:
        for v in mesh.faces[f].vertices:
            implicated_face_verts.add(v)
    for v in evs:
        for vn in vv[v]:
            epneighbors.add(vn)
    them=epneighbors.difference(implicated_face_verts)
    for v in them:
        for e in ve[v]:
            for vi in mesh.edges[e].key:
                if vi in evs:
                    ts.add(e)
    if ts.issubset(es):
        return []
    return ts-es
@e_lon.setter
def e_lon(mesh,L):
    raise AttributeError

@property
def life(mesh):
    ts=set()
    tx=set()
    vf=mesh.vf
    fs=mesh.fsel
    r=len(mesh.faces)
    d={i:set() for i in range(r)}
    for f in mesh.faces:
        for v in f.vertices:
            for n in vf[v]-{f.index}:
                if mesh.faces[n].select:
                    d[f.index].add(n)
    for i in d:
        L=len(d[i])
        if L ==3:
            ts.add(i)
        elif L !=2:
            tx.add(i)
    fs.update(ts)
    return fs-tx
@life.setter
def life(mesh,L):
    print(42)
    raise AttributeError

def kit_register():
    bpy.types.Mesh.eki=eki
    bpy.types.Mesh.vsel=vsel
    bpy.types.Mesh.esel=esel
    bpy.types.Mesh.fsel=fsel
    bpy.types.Mesh.vv=vv
    bpy.types.Mesh.ve=ve
    bpy.types.Mesh.vf=vf
    bpy.types.Mesh.ee=ee
    bpy.types.Mesh.ef=ef
    bpy.types.Mesh.ff=ff
    bpy.types.Mesh.svv=svv
    bpy.types.Mesh.see=see
    bpy.types.Mesh.sff=sff
    bpy.types.Mesh.je=je
    bpy.types.Mesh.jei=jei
    bpy.types.Mesh.e_lat=e_lat
    bpy.types.Mesh.e_lon=e_lon
    bpy.types.Mesh.life=life

def kit_unregister():
    del bpy.types.Mesh.eki
    del bpy.types.Mesh.vsel
    del bpy.types.Mesh.esel
    del bpy.types.Mesh.fsel
    del bpy.types.Mesh.vv
    del bpy.types.Mesh.ve
    del bpy.types.Mesh.vf
    del bpy.types.Mesh.ee
    del bpy.types.Mesh.ef
    del bpy.types.Mesh.ff
    del bpy.types.Mesh.svv
    del bpy.types.Mesh.see
    del bpy.types.Mesh.sff
    del bpy.types.Mesh.je
    del bpy.types.Mesh.jei
    del bpy.types.Mesh.e_lat
    del bpy.types.Mesh.e_lon
    del bpy.types.Mesh.life


class Registrant:pass


class polls_for_mesh:
    @classmethod
    def poll(self,context):
        try:
            assert context.active_object.type == 'MESH'
            return True
        except:
            return False


class MESH_OT_select_vertex_neighbors(Registrant,polls_for_mesh,bpy.types.Operator):
    """Hold shift to extend instead of replace selection"""
    bl_idname = "object.svv"
    bl_label = "Vertex Neighbors"
    bl_options = {'REGISTER','UNDO'}
    extend = bpy.props.BoolProperty()
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode = (True,False,False)
        bpy.ops.object.editmode_toggle()
        if self.extend:
            context.active_object.data.vsel = context.active_object.data.svv
        else:
            t=context.active_object.data.svv
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            context.active_object.data.vsel = t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
        
    def invoke(self,context,event):
        self.extend = event.shift
        return self.execute(context)


class MESH_OT_select_edge_neighbors(Registrant,polls_for_mesh,bpy.types.Operator):
    """Hold shift to extend instead of replace selection"""
    bl_idname = "object.see"
    bl_label = "Edge Neighbors"
    bl_options = {'REGISTER','UNDO'}
    extend = bpy.props.BoolProperty()
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode = (False,True,False)
        bpy.ops.object.editmode_toggle()
        if self.extend:
            context.active_object.data.esel = context.active_object.data.see
        else:
            t=context.active_object.data.see
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
        
    def invoke(self,context,event):
        self.extend = event.shift
        return self.execute(context)


class MESH_OT_select_face_neighbors(Registrant,polls_for_mesh,bpy.types.Operator):
    """Hold shift to extend instead of replace selection"""
    bl_idname="object.sff"
    bl_label="Face Neighbors"
    bl_options={'REGISTER','UNDO'}
    extend = bpy.props.BoolProperty()
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,False,True)
        bpy.ops.object.editmode_toggle()
        if self.extend:
            context.active_object.data.fsel=context.active_object.data.sff
        else:
            t=context.active_object.data.sff
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            context.active_object.data.fsel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
        
    def invoke(self,context,event):
        self.extend = event.shift
        return self.execute(context)


class MESH_OT_edges_lateral(Registrant,polls_for_mesh,bpy.types.Operator):
    """Hold shift to extend instead of replace selection"""
    bl_idname="object.elats"
    bl_label="Lateral Edge Neighbors"
    bl_options={'REGISTER','UNDO'}
    extend = bpy.props.BoolProperty()
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        if self.extend:
                    context.active_object.data.esel=context.active_object.data.e_lat
        else:
            t=context.active_object.data.e_lat
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
        
    def invoke(self,context,event):
        self.extend = event.shift
        return self.execute(context)


class MESH_OT_edges_longitudinal(Registrant,polls_for_mesh,bpy.types.Operator):
    """Hold shift to extend instead of replace selection"""
    bl_idname="object.elons"
    bl_label="Longitudinal Edge Neighbors"
    bl_options={'REGISTER','UNDO'}
    extend = bpy.props.BoolProperty()
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        if self.extend:
            context.active_object.data.esel=context.active_object.data.e_lon
        else:
            t=context.active_object.data.e_lon
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
        
    def invoke(self,context,event):
        self.extend = event.shift
        return self.execute(context)


class MESH_OT_just_edges(Registrant,polls_for_mesh,bpy.types.Operator):
    """Deselects faces and verts, leaving only edges selected."""
    bl_idname="object.just_edges"
    bl_label="Only the Edges"
    bl_options={'REGISTER','UNDO'}
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode = (False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.je
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        context.active_object.data.esel = t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class MESH_OT_inner_edges(Registrant,polls_for_mesh,bpy.types.Operator):
    """Reduce selection to inner edges"""
    bl_idname="object.inner_edges"
    bl_label="Inner Edges"
    bl_options={'REGISTER','UNDO'}
    
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.jei
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        context.active_object.data.esel = t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class MESH_OT_life(Registrant,polls_for_mesh,bpy.types.Operator):
    """Apply Conway's Life Algorithm to Face Selection."""
    bl_idname="object.life"
    bl_label="Conway's Life"
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode = (False,False,True)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.life
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        context.active_object.data.fsel = t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


def tk_draw(self,context):
    layout = self.layout
    layout.row().operator("object.svv")
    layout.row().operator("object.see")
    layout.row().operator("object.sff")
    layout.row().operator("object.elats")
    layout.row().operator("object.elons")
    layout.row().separator()
    layout.row().operator("object.just_edges")
    layout.row().operator("object.inner_edges")
    layout.row().separator()
    layout.row().operator("object.life")

class TopoKitMenu(bpy.types.Menu, Registrant):
    bl_idname="VIEW3D_MT_topokit_menu"
    bl_label="TopoKit"
    draw = tk_draw
        

def TK_ui_tog(self,context):
    if context.scene.tkui_show.in_v3d_tools:
        bpy.types.VIEW3D_PT_tools_meshedit.append(tk_draw)
    else:
        bpy.types.VIEW3D_PT_tools_meshedit.remove(tk_draw)
    return None
        
        
class TK_ui_vis_prefs(bpy.types.PropertyGroup,Registrant):
    in_v3d_tools = bpy.props.BoolProperty(description='Toggles display of buttons in the v3d tools pane',name='show ui in tools pane',update=TK_ui_tog)


class TopoKitUI_prefs(bpy.types.Panel, Registrant):
    bl_label = "Topokit Settings"
    bl_space_type,bl_region_type=("VIEW_3D","UI")
    def draw(self,context):
        self.layout.row().prop(context.scene.tkui_show, 'in_v3d_tools')


def topokit_menu(self,context):
    self.layout.menu("VIEW3D_MT_topokit_menu")

def register():
    kit_register()
    list(map(bpy.utils.register_class, Registrant.__subclasses__()))
    bpy.types.Scene.tkui_show = bpy.props.PointerProperty(type=TK_ui_vis_prefs)
    
    bpy.types.VIEW3D_PT_tools_meshedit.append(tk_draw)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(topokit_menu)

def unregister():
    kit_unregister()
    list(map(bpy.utils.unregister_class,Registrant.__subclasses__()))
    del bpy.types.Scene.tkui_show
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(topokit_menu)
    bpy.types.VIEW3D_PT_tools_meshedit.remove(tk_draw)

if __name__=="__main__":
    register()