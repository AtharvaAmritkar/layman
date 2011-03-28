#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# LAYMAN DARCS OVERLAY HANDLER
#################################################################################
# File:       darcs.py
#
#             Handles darcs overlays
#
# Copyright:
#             (c) 2005 - 2008 Gunnar Wrobel, Andres Loeh
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Gunnar Wrobel <wrobel@gentoo.org>
#             Andres Loeh <kosmikus@gentoo.org>
#
''' Darcs overlay support.'''

__version__ = "$Id: darcs.py 236 2006-09-05 20:39:37Z wrobel $"

#===============================================================================
#
# Dependencies
#
#-------------------------------------------------------------------------------

from   layman.utils             import path
from   layman.overlays.source   import OverlaySource, require_supported

#===============================================================================
#
# Class BzrOverlay
#
#-------------------------------------------------------------------------------

class DarcsOverlay(OverlaySource):
    ''' Handles darcs overlays.'''

    type = 'Darcs'
    type_key = 'darcs'

    def __init__(self, parent, config, _location, ignore = 0, quiet = False):

        super(DarcsOverlay, self).__init__(parent, config,
            _location, ignore, quiet)

    def add(self, base, quiet = False):
        '''Add overlay.'''

        self.supported()

        cfg_opts = self.config["darcs_addopts"]
        target = path([base, self.parent.name])

        # darcs get --partial SOURCE TARGET
        if len(cfg_opts):
            args = ['get', '--partial', cfg_opts,
                self.src + '/', target]
        else:
            args = ['get', '--partial',
                self.src + '/', target]

        return self.postsync(
            self.run_command(self.command(), *args, cmd=self.type),
            cwd=target)

    def sync(self, base, quiet = False):
        '''Sync overlay.'''

        self.supported()

        cfg_opts = self.config["darcs_addopts"]
        target = path([base, self.parent.name])

        # darcs pull --all SOURCE
        if len(cfg_opts):
            args = ['pull', '--all', cfg_opts, self.src]
        else:
            args = ['pull', '--all', self.src]
        return self.postsync(
            self.run_command(self.command(), *args, cwd=target, cmd=self.type),
            cwd=target)

    def supported(self):
        '''Overlay type supported?'''

        return require_supported(
            [(self.command(),  'darcs', 'dev-vcs/darcs'),],
            self.output.error)
