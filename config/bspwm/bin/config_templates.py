# config_templates.py

def dunst_config(main, bg, fg):
    return f"""[global]
    font = JetBrainsMono Nerd Font 10
    format = "<b>%a</b>\\n%s\\n%b"
    notification_limit = 5

    progress_bar = true
    progress_bar_height = 6

    frame_color = "{main}"

    transparency = 0

[urgency_low]
    background = "{bg}"
    foreground = "{bg}"
    timeout = 5

[urgency_normal]
    foreground = "{fg}"
    timeout = 8
    background = "{bg}"

[urgency_critical]
    frame_color = "{main}"
    background = "{bg}"
    foreground = "{bg}"
    timeout = 0
"""


def rofi_config(main, bg, fg, secondary):
    return f"""* {{
    font: "JetBrainsMono Nerd Font 11";
    main: {main};
    bg: {bg};
    fg: {fg};
    bg-alt: {bg};
    secondary-text: {secondary};
}}
"""

def fastfetch_config(main_ansi, font_ansi):
    return f"""{{
  "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/master/doc/json_schema.json",
  "logo": {{
    "type": "none"
  }},
  "display": {{
    "separator": ": ",
    "color": {{
      "keys": "{main_ansi}",
      "title": "{main_ansi}",
      "output": "{font_ansi}"
    }},
    "percent": {{
      "type": 9,
      "color": {{
        "green": "{font_ansi}",
        "yellow": "{font_ansi}",
        "red": "{font_ansi}"
      }}
    }}
  }},
  "modules": [
    "title",
    "separator",
    "os",
    "host",
    "kernel",
    "uptime",
    "packages",
    "shell",
    "display",
    "wm",
    "cursor",
    "terminal",
    "terminalfont",
    "cpu",
    "gpu",
    "memory",
    "swap",
    "disk",
    "localip",
    "locale",
    "break"
  ]
}}"""

def kitty_config():
    return """font_family JetBrainsMono NF
font_size 10.5
enable_audio_bell no
bell_on_tab "[sound] "
remember_window_size  no
window_border_width 1pt
draw_minimal_borders yes
window_padding_width 10
inactive_text_alpha 0.6
hide_window_decorations yes
confirm_os_window_close 0
#tcursor_shape block
cursor_stop_blinking_after 0
scrollback_lines 2000
copy_on_select yes
mouse_hide_wait 0
select_by_word_characters @-./_~?&=%+#a
#ab_bar_style powerline
"""


def polybar_config():
    return r""";==========================================================
;
;
;   ██████╗  ██████╗ ██╗  ██╗   ██╗██████╗  █████╗ ██████╗
;   ██╔══██╗██╔═══██╗██║  ╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗
;   ██████╔╝██║   ██║██║   ╚████╔╝ ██████╔╝███████║██████╔╝
;   ██╔═══╝ ██║   ██║██║    ╚██╔╝  ██╔══██╗██╔══██║██╔══██╗
;   ██║     ╚██████╔╝███████╗██║   ██████╔╝██║  ██║██║  ██║
;   ╚═╝      ╚═════╝ ╚══════╝╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
;
;
;   To learn more about how to configure Polybar
;   go to https://github.com/polybar/polybar
;
;   The README contains a lot of information
;
;==========================================================

[colors]
background = #000000
background-alt = #373B41
foreground = #C5C8C6
primary = ${env:MAIN_COLOR:#329DA4}
secondary = #8ABEB7
alert = #A54242
disabled = #707880

[bar/main]
monitor = ${env:MONITOR:}
wm-restack = bspwm
width = 100%
height = 24pt
radius = 6

; dpi = 96

background = ${colors.background}
foreground = ${colors.foreground}

#line-size = 3ptoverride-redirect = false

border-size = 4pt
border-color = #00000000

padding-left = 0
padding-right = 1

module-margin = 1

separator = " "
separator-foreground = ${colors.disabled}

#font-0 = monospace;2
font-0 = "JetBrainsMono Nerd Font:style=Regular:size=10;2"
font-1 = "Font Awesome 6 Free:style=Solid:size=10;2"
font-2 = "Noto Sans:size=10;2"
font-3 = "DejaVu Sans:size=10;2"

#modules-left = xworkspaces xwindow
#modules-left = xworkspaces systray
modules-left = bspwm systray

modules-center = cpu memory filesystem battery
#modules-right = xkeyboard wlan eth pulseaudio date scripts 
modules-right = xkeyboard wlan eth pulseaudio date notifications theme-toggle background_select scripts power


cursor-click = pointer
cursor-scroll = ns-resize

enable-ipc = true

; wm-restack = generic
; wm-restack = bspwm
; wm-restack = i3

; override-redirect = true
# override-redirect = true
override-redirect = false

[module/systray]
type = internal/tray

format-margin = 4pt
tray-spacing = 6pt
tray-maxsize = 5

[module/notifications]
type = custom/script
exec = echo "󰂚"
click-left = dunstctl history-pop
format = <label>
label-foreground = ${colors.primary}

[module/scripts]
type = custom/script
exec = echo ""
format = <label>
label = %output%
label-foreground = ${colors.primary}
click-left = ~/.config/bspwm/bin/rofi_custom_script.py

[module/background_select]
type = custom/script
exec = echo ""
format = <label>
label = %output%
label-foreground = ${colors.primary}
click-left = ~/.config/bspwm/bin/rofi_choose_background.py

[module/theme-toggle]
type = custom/script
exec = ~/.config/bspwm/bin/polybar_current_theme.py
click-left = ~/.config/bspwm/bin/custom_script_change_theme_dark_or_light.py
label = %output%
format = <label>
label-foreground = ${colors.primary}

[module/battery]
type = internal/battery
full-at = 99
battery = ${system.sys_battery}
adapter = ${system.sys_adapter}
poll-interval = 2
time-format = %H:%M
 
format-charging = <animation-charging><label-charging>
label-charging = " %percentage%%"

format-discharging = <ramp-capacity><label-discharging>
label-discharging = " %percentage%%"

format-full = <label-full>
format-full-prefix = 
format-full-prefix-foreground = ${colors.primary}
label-full = " %percentage%%"

ramp-capacity-0 = 
ramp-capacity-1 = 
ramp-capacity-2 = 
ramp-capacity-3 = 
ramp-capacity-4 = 
ramp-capacity-foreground = ${colors.primary}
ramp-capacity-font = 2

animation-charging-0 = 
animation-charging-1 = 
animation-charging-2 = 
animation-charging-3 = 
animation-charging-4 = 
animation-charging-foreground = ${colors.primary}
animation-charging-font = 2
animation-charging-framerate = 700

[module/bspwm]
type = internal/bspwm

pin-workspaces = true
enable-click = true
enable-scroll = true
reverse-scroll = false

label-focused = ""
label-focused-foreground = ${colors.primary}
label-focused-underline = ${colors.primary}
label-focused-padding = 1

label-occupied = ""
label-occupied-padding = 1

label-urgent = ""
label-urgent-foreground = ${colors.primary}
label-urgent-padding = 1

label-empty = ""
label-empty-padding = 1

[module/filesystem]
type = internal/fs
interval = 25

mount-0 = /

format-mounted = <label-mounted>
format-mounted-prefix =  
format-mounted-prefix-foreground = ${colors.primary}

label-mounted = "  %percentage_used%%"

format-unmounted = <label-unmounted>
label-unmounted = %mountpoint% not mounted
label-unmounted-foreground = ${colors.disabled}

[module/pulseaudio]
type = internal/pulseaudio

format-volume-prefix = "  "
format-volume = <label-volume>

label-volume = %percentage%%

label-muted =  muted

[module/xkeyboard]
type = internal/xkeyboard
blacklist-0 = num lock

label-layout = %layout%

label-indicator-padding = 2
label-indicator-margin = 1
label-indicator-foreground = ${colors.background}
label-indicator-background = ${colors.secondary}

[module/memory]
type = internal/memory
interval = 2
format-prefix = "󰘚 "
format-prefix-foreground = ${colors.primary}
label = %percentage_used:2%%

[module/cpu]
type = internal/cpu
interval = 2
format-prefix = ""
format-prefix-foreground = ${colors.primary}
label = " %percentage:2%%"

[network-base]
type = internal/network
interval = 5
format-connected = <label-connected>
format-disconnected = <label-disconnected>
label-disconnected = %{F#F0C674}%ifname%%{F#707880} disconnected

[module/wlan]
inherit = network-base
interface-type = wireless

format-connected = %{A1:nm-connection-editor &:}<label-connected>%{A}

label-connected =   ↓%downspeed% ↑%upspeed%

interval = 1

[module/eth]
inherit = network-base
interface-type = wired

format-connected = %{A1:nm-connection-editor &:}<label-connected>%{A}

label-connected = 󰌗 ↓%downspeed% ↑%upspeed%

[module/date]
type = custom/script
exec = date "+%I:%M:%S %p"
interval = 1

format = <label>
label = %output%

click-left = ~/.config/bspwm/bin/script_calendar.py

[settings]
screenchange-reload = true
#screenchange-reload = false
pseudo-transparency = false

[module/power]
type = custom/script
exec = echo ""
format = <label>
label = %output%
label-foreground = ${colors.primary}
click-left = ~/.config/bspwm/bin/rofi_powermenu.py

; vim:ft=dosini
"""
