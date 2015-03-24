# -*- coding: utf-8 -*-
import os
import pymel.core as pm
from optionsWindow import OptionsWindow
from jsonFile import JsonFile


def nurbsToPolySp(*args, **kwds):
    """
    nurbsToPolySp v0.0.1

    - Select nurbsSurface or transform what have nurbsSurfaces before execute this function.
    - Converted polygon's name will change to nurbsSurface's name.
    - NurbsSurface's name will add prefix and add suffix.
    - Converted polygon parent will nurbsSurface's parent.
    - Converted polygon's polygonType to Quads.
    - Converted polygon's tessellate will nurbsSurface's matchRenderTesselation.
    """
    # get options from args.
    selected = False
    before_sels = None
    if len(args) > 0:
        sels = pm.ls(args)
        before_sels = pm.ls(sl=True)
    else:
        sels = pm.ls(sl=True)
        selected = True
    if 1 > len(sels):
        raise Exception(u'Please select one or more what is group have nurbsSurface.')
 
    # get options from kwds.
    if u'prefix' in kwds:
        prefix = kwds[u'prefix']
    else:
        prefix = u''
    if u'suffix' in kwds:
        suffix = kwds[u'suffix']
    else:
        suffix = u'Nrb'
 
    # main compute.
    message = []
    for sel in sels:
        nurbs_shapes = pm.listRelatives(sel, allDescendents=True, type=u'nurbsSurface')
        if 1 > len(nurbs_shapes):
            message.append(u'{0} have not nurbsSurface. skipped.'.format(sel))
            continue
        for nurbs_shape in nurbs_shapes:
            mesh_name = pm.nurbsToPoly(nurbs_shape,
                                       matchRenderTessellation=True,
                                       constructionHistory=True)
            mesh = pm.ls(mesh_name)[0]
            mesh_shape = mesh.getShape()
            tessellate = mesh_shape.inputs()[0]
            tessellate.setAttr('polygonType', lock=False)
            tessellate.setAttr('polygonType', 1)
 
            nurbs = nurbs_shape.getParent()
            nurbs_parent = nurbs.getParent()
            if nurbs_parent is not None:
                pm.parent(mesh, nurbs_parent)
 
            name = nurbs.name()
            pm.rename(nurbs, prefix + name + suffix)
            message.append(u'NurbsSurface renamed: "{0}" -> "{1}"'.format(name, prefix + name + suffix))
            pm.rename(mesh, name)
            message.append(u'Create polygon mesh:"{0}"'.format(name))
    if selected:
        pm.select(sels)
    else:
        pm.select(before_sels)
    print '\n'.join(message)
    print u'Finished nurbsToPolySp!!'


class NurbsToPolySpOptionsWindow(OptionsWindow):
    def __init__(self):
        super(NurbsToPolySpOptionsWindow, self).__init__()
        self.name = u'nurbsToPolySpOptionsWindow'
        self.title = u'Nurbs to poly SP Options Window'
        self.jsonFile = JsonFile(NurbsToPolySpOptionsWindow.getFilePath())
        self.pre = None
        self.post = None
        self.prefix = None
        self.suffix = None
 
    @classmethod
    def getFilePath(cls):
        p = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(p, u'nurbsToPolySpOptionsWindow.json')
 
    def displayOptions(self):
        self.setSelfFromFile()
        layout = pm.columnLayout()
        with layout:
            self.prefix = pm.textFieldGrp(
                label=u'Prefix',
                text=self.pre
            )
            self.suffix = pm.textFieldGrp(
                label=u'Suffix',
                text=self.post
            )
 
    def setSelfFromUI(self):
        self.pre = pm.textFieldGrp(self.prefix, query=True, text=True)
        self.post = pm.textFieldGrp(self.suffix, query=True, text=True)
 
    def setSelfFromFile(self):
        data = self.jsonFile.load()
        if data is None:
            data = dict(pre=u'', post=u'Nrb')
        self.pre = data[u'pre']
        self.post = data[u'post']
 
    def applyBtnCmd(self, *args):
        self.editMenuSaveCmd()
        nurbsToPolySp(prefix=self.pre, suffix=self.post)
 
    def editMenuSaveCmd(self, *args):
        self.setSelfFromUI()
        self.jsonFile.save(
            pre=self.pre,
            post=self.post
        )
 
    def editMenuResetCmd(self, *args):
        pm.textFieldGrp(self.prefix, edit=True, text=u'')
        pm.textFieldGrp(self.suffix, edit=True, text=u'Nrb')
        self.jsonFile.delete()
