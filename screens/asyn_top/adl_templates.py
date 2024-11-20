WINDOW_WIDTH8 = 165
WINDOW_WIDTH16 = 340
adl_header = """
file {
	name="$(FILENAME)"
	version=030111
}
display {
	object {
		x=1188
		y=965
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
}"""

adl_row8 = """
"text update" {
	object {
		x=35
		y=$(Y)
		width=125
		height=25
	}
	monitor {
		chan="$(P)$(R$(N)).PORT"
		clr=14
		bclr=2
	}
	align="horiz. centered"
	limits {
	}
}
"related display" {
	object {
		x=5
		y=$(Y)
		width=25
		height=25
	}
	display[0] {
		label="asyn $(N)"
		name="asynOctet"
		args="P=$(P),R=$(R$(N))"
	}
	clr=0
	bclr=63
	label="-$(N)"
}"""

adl_row16 = """
"text update" {
	object {
		x=35
		y=$(Y)
		width=125
		height=25
	}
	monitor {
		chan="$(P)$(R$(N1)).PORT"
		clr=14
		bclr=2
	}
	align="horiz. centered"
	limits {
	}
}
"related display" {
	object {
		x=5
		y=$(Y)
		width=25
		height=25
	}
	display[0] {
		label="asyn $(N)"
		name="asynOctet"
		args="P=$(P),R=$(R$(N1))"
	}
	clr=0
	bclr=63
	label="-$(N1)"
}
"text update" {
	object {
		x=205
		y=$(Y)
		width=125
		height=25
	}
	monitor {
		chan="$(P)$(R$(N2)).PORT"
		clr=14
		bclr=2
	}
	align="horiz. centered"
	limits {
	}
}
"related display" {
	object {
		x=175
		y=$(Y)
		width=25
		height=25
	}
	display[0] {
		label="asyn $(N2)"
		name="asynOctet"
		args="P=$(P),R=$(R$(N2))"
	}
	clr=0
	bclr=63
	label="-$(N2)"
}
"""
