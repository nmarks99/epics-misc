WINDOW_WIDTH = 120
adl_header = """
file {
	name="$(FILENAME)"
	version=030111
}
display {
	object {
		x=1000
		y=1000
		width=$(WINDOW_WIDTH)
		height=$(WINDOW_HEIGHT)
	}
	clr=14
	bclr=4
	cmap=""
	gridSpacing=5
	gridOn=1
	snapToGrid=1
}
"color map" {
	ncolors=65
	colors {
		ffffff,
		ececec,
		dadada,
		c8c8c8,
		bbbbbb,
		aeaeae,
		9e9e9e,
		919191,
		858585,
		787878,
		696969,
		5a5a5a,
		464646,
		2d2d2d,
		000000,
		00d800,
		1ebb00,
		339900,
		2d7f00,
		216c00,
		fd0000,
		de1309,
		be190b,
		a01207,
		820400,
		5893ff,
		597ee1,
		4b6ec7,
		3a5eab,
		27548d,
		fbf34a,
		f9da3c,
		eeb62b,
		e19015,
		cd6100,
		ffb0ff,
		d67fe2,
		ae4ebc,
		8b1a96,
		610a75,
		a4aaff,
		8793e2,
		6a73c1,
		4d52a4,
		343386,
		c7bb6d,
		b79d5c,
		a47e3c,
		7d5627,
		58340f,
		99ffff,
		73dfff,
		4ea5f9,
		2a63e4,
		0a00b8,
		ebf1b5,
		d4db9d,
		bbc187,
		a6a462,
		8b8239,
		73ff6b,
		52da3b,
		3cb420,
		289315,
		1a7309,
	}
}
"""

adl_row_pump = """
text {
	object {
		x=30
		y=$(Y)
		width=80
		height=20
	}
	"basic attribute" {
		clr=14
	}
	textix="$(LABEL)"
}
"related display" {
	object {
		x=5
		y=$(Y)
		width=20
		height=20
	}
	display[0] {
		label="display"
		name="Pump.adl"
		args="P=$(PREFIX),PUMP=$(PUMP)"
	}
	clr=14
	bclr=4
}
"""

adl_row_gauge = """
text {
	object {
		x=30
		y=$(Y)
		width=80
		height=20
	}
	"basic attribute" {
		clr=14
	}
	textix="$(LABEL)"
}
"related display" {
	object {
		x=5
		y=$(Y)
		width=20
		height=20
	}
	display[0] {
		label="display"
		name="VacSen.adl"
		args="P=$(PREFIX),GAUGE=$(GAUGE)"
	}
	clr=14
	bclr=4
}
"""

