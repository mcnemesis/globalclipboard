res:
	pyrcc4 -o gclip_resources_rc.py resources/gclip_resources.qrc

ui: res
	pyuic -o gclip_ui.py -e qtui/gclip_ui.ui
	#some changes I found necessary to make to the generated files prior to using em
	sed -i '/setSizeGripEnabled(False)/{s/\(\s*\)\(\W\+.*\)/\1#\2/g}' gclip_ui.py
	sed -i '/self\.resize/{s/\(\s*\)\(\W\+.*\)/\1#\2/g}' gclip_ui.py
	sed -i '/GClipDialog\.setWindowTitle/{s/GClipDialog/self/g}' gclip_ui.py
	sed -i '/GClipDialog\.setWindowIcon/{s/GClipDialog/self/g}' gclip_ui.py

testui: ui
	python gclip_ui.py

testgclip: ui
	python gclip.py

clean:
	rm gclip_ui.py* gclip_resources_rc.py*
