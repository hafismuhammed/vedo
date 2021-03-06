from __future__ import division, print_function

import vtk
import vedo.docs as docs
from vedo.base import Base3DProp
import vedo.utils as utils

__doc__ = (
    """
Submodule extending the ``vtkAssembly`` object functionality.
"""
    + docs._defs
)

__all__ = ["Assembly"]


#################################################
class Assembly(vtk.vtkAssembly, Base3DProp):
    """Group many meshes as a single new mesh as a ``vtkAssembly``.

    |gyroscope1| |gyroscope1.py|_
    """

    def __init__(self, *meshs):

        vtk.vtkAssembly.__init__(self)
        Base3DProp.__init__(self)

        if len(meshs) == 1:
            meshs = meshs[0]
        else:
            meshs = utils.flatten(meshs)

        self.actors = meshs

        if len(meshs) and hasattr(meshs[0], "top"):
            self.base = meshs[0].base
            self.top = meshs[0].top
        else:
            self.base = None
            self.top = None

        for a in meshs:
            if a:
                self.AddPart(a)

    def __add__(self, meshs):
        if isinstance(meshs, list):
            for a in meshs:
                self.AddPart(a)
        else:  # meshs=one mesh
            self.AddPart(meshs)
        return self


    def clone(self):
        """Make a clone copy of the object."""
        newlist = []
        for a in self.actors:
            newlist.append(a.clone())
        return Assembly(newlist)


    def unpack(self, i=None):
        """Unpack the list of objects from a ``Assembly``.

        If `i` is given, get `i-th` object from a ``Assembly``.
        Input can be a string, in this case returns the first object
        whose name contains the given string.

        |customIndividualAxes| |customIndividualAxes.py|_
        """
        if i is None:
            return self.actors
        elif isinstance(i, int):
            return self.actors[i]
        elif isinstance(i, str):
            for m in self.actors:
                if i in m.name:
                    return m
        return None


    def lighting(self, style='', ambient=None, diffuse=None,
                 specular=None, specularPower=None, specularColor=None):
        """Set the lighting type to all ``Mesh`` in the ``Assembly`` object.

        :param str style: preset style, can be `[metallic, plastic, shiny, glossy]`
        :param float ambient: ambient fraction of emission [0-1]
        :param float diffuse: emission of diffused light in fraction [0-1]
        :param float specular: fraction of reflected light [0-1]
        :param float specularPower: precision of reflection [1-100]
        :param color specularColor: color that is being reflected by the surface
        """
        for a in self.actors:
            a.lighting(style, ambient, diffuse,
                       specular, specularPower, specularColor)
        return self

