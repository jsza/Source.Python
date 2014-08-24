# ../cvars/__init__.py

"""Provides access to ConVar instances and the ability to create a ConVar."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from _cvars import _ConVar
from cvars.flags import ConVarFlags


# =============================================================================
# >> FORWARD IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from _cvars import Cvar
from _cvars import ConCommandBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('ConCommandBase',
           'ConVar',
           'Cvar',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class ConVar(_ConVar):

    """ConVar wrapper to provide easy access to cvars."""

    def __init__(
            self, name, value='0', flags=0,
            description='', min_value=None, max_value=None):
        """Called when a server-var is initilized."""
        super(ConVar, self).__init__(
            name, value, flags, description,
            min_value is not None, min_value or 0.0,
            max_value is not None, max_value or 0.0)

    def __getattr__(self, attr):
        """Retrieve the value of the given attribute."""
        # Get the flag
        flag = getattr(ConVarFlags, attr.upper(), None)

        # Is the attribute a flag?
        if flag is not None:

            # Return the value of the cvar's flag
            return self.is_flag_set(flag)

        # If not, raise an error
        raise AttributeError(
            '"ConVar" object has no attribute "{0}"'.format(attr))

    def __setattr__(self, attr, value):
        """Set the value of the given attribute."""
        # Get the flag
        flag = getattr(ConVarFlags, attr.upper(), None)

        # Is the attribute a flag?
        if flag is None:

            # Does the instance itself have the attribute?
            if not hasattr(self, attr):

                # If not, raise an error
                raise AttributeError(
                    '"ConVar" object has no attribute "{0}"'.format(attr))

            # Set the attribute
            super(ConVar, self).__setattr__(attr, value)

            # No need to go further
            return

        # Is the value "True"
        if value:

            # Add the flag
            self.add_flags(flag)

            # No need to go further
            return

        # Remove the flag
        self.remove_flags(flag)

    def make_public(self):
        """Set the notify flag for the cvar."""
        self.add_flags(ConVarFlags.NOTIFY)