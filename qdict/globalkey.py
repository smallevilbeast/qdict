#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from Xlib import X, XK
from Xlib.display import Display
from threading import Lock
import saferef
import weakref

WEAKREF_TYPES = (weakref.ReferenceType, saferef.BoundMethodWeakref)


global_key_running = True
global_key_lock = Lock()

def enable_global_key():
    '''
    Enable global key.
    '''
    global global_key_running

    global_key_lock.acquire()
    global_key_running = True
    global_key_lock.release()

def disable_global_key():
    '''
    Disable global key.
    '''
    global global_key_running

    global_key_lock.acquire()
    global_key_running = False
    global_key_lock.release()

class GlobalKey(threading.Thread):
    
    def __init__(self):
        super(GlobalKey, self).__init__()
        self.setDaemon(True)
        self.disp = Display()
        self.root = self.disp.screen().root
        self._binding_map = {}
        
        self.stop = False
        
        self.known_modifiers_mask = 0
        
        x_modifiers = (X.ControlMask,
                       X.ShiftMask,
                       X.Mod1Mask,
                       X.Mod2Mask,
                       X.Mod3Mask,
                       X.Mod4Mask,
                       X.Mod5Mask,
                       )
        
        for mod in x_modifiers:
            self.known_modifiers_mask |= mod
            
    def bind(self, binding_string, action, weak=False):        
        keyval, modifiers = self.parse_keystring(binding_string)
        keycode = self.disp.keysym_to_keycode(keyval)
        
        if weak:
            action = saferef.Ref(action)
        
        # Binding key.
        self._binding_map[(keycode, modifiers)] = action
        
        num_lock_modifiers = modifiers | X.Mod2Mask
        self._binding_map[(keycode, num_lock_modifiers)] = action
        
        # Restart grab keybinding.
        self.regrab()
        
    def unbind(self, binding_string):
        '''
        '''
        
        keyval, modifiers = self.parse_keystring(binding_string)
        keycode = self.disp.keysym_to_keycode(keyval)
        
        num_lock_modifiers = modifiers | X.Mod2Mask

        # Remove keybinding from binding map.
        regrab_flag = False
        if self._binding_map.has_key((keycode, modifiers)):
            del self._binding_map[(keycode, modifiers)]
            regrab_flag = True

        # Try remove key binding (with Num-Lock mask) from binding map.
        if self._binding_map.has_key((keycode, num_lock_modifiers)):
            del self._binding_map[(keycode, num_lock_modifiers)]
            regrab_flag = True

        if regrab_flag:
            self.regrab()
            
    def grab(self):
        '''
        Grab key.
        '''
        for (keycode, modifiers) in self._binding_map.keys():
            try:
                self.root.grab_key(keycode, int(modifiers), True, X.GrabModeAsync, X.GrabModeSync)
            except Exception, e:
                print "function grab got error: %s" % (e)
                
    def ungrab(self):
        '''
        Ungrab key.
        '''
        for (keycode, modifiers) in self._binding_map.keys():
            try:
                self.root.ungrab_key(keycode, modifiers, self.root)
            except Exception, e:
                print "function ungrab got error: %s" % (e)
                
    def regrab(self):
        '''
        Regrab key.
        '''
        self.ungrab()
        self.grab()
    
    def run(self):
        '''
        GlobalKey thread loop.
        '''
        global global_key_running

        wait_for_release = False
        while not self.stop:
            event = self.disp.next_event()
            if global_key_running:
                if event.type == X.KeyPress and not wait_for_release:
                    keycode = event.detail
                    modifiers = event.state & self.known_modifiers_mask
                    try:
                        action = self._binding_map[(keycode, modifiers)]
                    except KeyError:
                        self.disp.allow_events(X.ReplayKeyboard, event.time)
                    else:
                        wait_for_release = True
                        self.disp.allow_events(X.AsyncKeyboard, event.time)
                        self._upcoming_action = (keycode, modifiers, action)

                elif event.type == X.KeyRelease and wait_for_release and event.detail == self._upcoming_action[0]:
                    wait_for_release = False
                    action = self._upcoming_action[2]
                    if isinstance(action, WEAKREF_TYPES):
                        action = action()
                    del self._upcoming_action
                    action()
                    self.disp.allow_events(X.AsyncKeyboard, event.time)
                else:
                    self.disp.allow_events(X.ReplayKeyboard, event.time)
            else:
                self.disp.allow_events(X.ReplayKeyboard, event.time)

    def exit(self):
        '''
        Exit global key.
        '''
        self.stop = True
        self.ungrab()
        self.disp.close()
        
    def parse_keystring(self, keystring):
        keys = keystring.split(" + ")
        if len(keys) == 1:
            keyval = XK.string_to_keysym(keys[0].upper())
            modifier_mask = 0
        else:    
            keyval = XK.string_to_keysym(keys[-1].upper())
            modifier_mask = 0
            
            if "Ctrl" in keys[0:-1]:
                modifier_mask |= X.ControlMask
            if "Alt"  in keys[0:-1]:
                modifier_mask |= X.Mod1Mask
            
        # modifier_mask |= X.ShiftMask        
        return (keyval, modifier_mask)
        
    def string_to_keycode(self, key):
        codes_mod=[50,62,64,108,37,105]
        names_mod=['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Control_L', 'Control_R']
        if key in names_mod:
           return codes_mod[names_mod.index(key)]
        keys_special={' ':'space','\t':'Tab','\n':'Return','\r':'BackSpace','\e':'Escape',
                      '!':'exclam','#':'numbersign','%':'percent','$':'dollar','&':'ampersand','"':'quotedbl',
                      '\'':'apostrophe','(':'parenleft',')':'parenright','*':'asterisk','=':'equal','+':'plus',
                      ',':'comma','-':'minus','.':'period','/':'slash',':':'colon',';':'semicolon','<':'less',
                      '>':'greater','?':'question','@':'at','[':'bracketleft',']':'bracketright','\\':'backslash',
                      '^':'asciicircum','_':'underscore','`':'grave','{':'braceleft','|':'bar','}':'braceright',
                      '~':'asciitilde'
                     }
        key_sym=XK.string_to_keysym(key)
        if key_sym==0:
           key_sym=XK.string_to_keysym(keys_special[key])
        return self.disp.keysym_to_keycode(key_sym)
    
    def keycode_to_string(self, key_code):
        codes_mod=[50,62,64,108,37,105,113,111,114,116,110,115,112,117,118,119,107,
                   67,68,69,70,71,72,73,74,75,76,95,96
                  ]
        names_mod=['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Control_L', 'Control_R',
                   'Left', 'Up', 'Right', 'Down', 'Home', 'End', 'Page_Up', 'Page_Down',
                   'Insert', 'Delete', 'Print',
                   'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12'
                  ]
        if key_code in codes_mod:
           return names_mod[codes_mod.index(key_code)]
        #2nd: 0 is unshifted, 1 is shifted, 2 is alt grid, and 3 is shiftalt grid
        return XK.keysym_to_string(self.disp.keycode_to_keysym(key_code, 0))        
    
