""" xmlasdict

.. module:: xmlasdict
    :synopsis: python library to read xml DOM trees as dicts (with iter and gettattribute behaviour)
    :noindex:

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""

from .parser import parse
from .wrapper import Wrapper, IterWrapper
from .__version__ import __version__
import logging

__all__ = ['parse', 'Wrapper', 'IterWrapper', '__version__']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
