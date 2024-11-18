adl_header = """
file {
	name="$(FILENAME)"
	version=030111
}
display {
	object {
		x=946
		y=1053
		width=250
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

template_soft = """
text {
	object {
		x=5
		y=$(Y)
		width=130
		height=30
	}
	"basic attribute" {
		clr=14
	}
	textix="$(IOC)"
}
"related display" {
	object {
		x=160
		y=$(Y)
		width=30
		height=30
	}
	display[0] {
		label="Soft IOC Status"
		name="ioc_stats_soft.adl"
		args="ioc=$(IOC),P=$(IOC):"
	}
	display[1] {
		label="Debug screen"
		name="$(IOC).ui"
		args="P=$(IOC):"
	}
	clr=14
	bclr=4
}
oval {
	object {
		x=200
		y=$(Y)
		width=30
		height=30
	}
	"basic attribute" {
		clr=15
	}
	"dynamic attribute" {
		vis="if not zero"
		chan="$(IOC):$(UP_PV)"
	}
}"""

template_vme = """
text {
	object {
		x=5
		y=$(Y)
		width=130
		height=30
	}
	"basic attribute" {
		clr=14
	}
	textix="$(IOC)"
}
"related display" {
	object {
		x=160
		y=$(Y)
		width=30
		height=30
	}
	display[1] {
		label="vxWorks IOC status"
		name="ioc_stats_vxworks.adl"
		args="ioc=$(IOC),P=$(IOC):"
	}
	display[2] {
		label="Debug screen"
		name="$(IOC).ui"
		args="P=$(IOC):"
	}
	clr=14
	bclr=4
}
oval {
	object {
		x=200
		y=$(Y)
		width=30
		height=30
	}
	"basic attribute" {
		clr=15
	}
	"dynamic attribute" {
		vis="if not zero"
		chan="$(IOC):$(UP_PV)"
	}
}"""
