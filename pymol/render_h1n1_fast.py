# /// script
# requires-python = ">=3.10, <3.13"
# dependencies = [
#     "pymol-open-source-whl",
# ]
# ///

import os
import sys

os.environ["PYOPENGL_PLATFORM"] = "osmesa"

import pymol
pymol.pymol_argv = ["pymol", "-cq"]
pymol.finish_launching()

from pymol import cmd

structure_file = "/Users/sophiadeomena/.gemini/antigravity/brain/0784b279-2fc2-4198-905d-f807d5f78ba2/1RU7/pdb_00001ru7.cif"
output_dir = "/Users/sophiadeomena/.gemini/antigravity/brain/0784b279-2fc2-4198-905d-f807d5f78ba2/pymol_output"
os.makedirs(output_dir, exist_ok=True)

cmd.load(structure_file, "ha_1918_h1n1")
cmd.remove("solvent")

# Global aesthetics
cmd.bg_color("black")
cmd.set("ray_opaque_background", 1)
cmd.set("antialias", 1)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_highlight_color", "grey60")
cmd.set("depth_cue", 1)
cmd.set("fog_start", 0.5)

# Render 1: Trimer with HA1 (Heads) in cyan/teal and HA2 (Stems) in blue/marine
cmd.show_as("cartoon", "all")
cmd.color("cyan", "chain A")
cmd.color("teal", "chain C")
cmd.color("aquamarine", "chain E")
cmd.color("marine", "chain B")
cmd.color("slate", "chain D")
cmd.color("deepblue", "chain F")
cmd.orient("all")
cmd.turn("y", 35)
cmd.png(f"{output_dir}/ha_trimer_cartoon.png", width=1400, height=1050, dpi=150)
print("1. Rendered ha_trimer_cartoon.png")

# Render 2: Functional Sites (Sialic acid pocket & Fusion peptide)
cmd.select("rbs", "chain A+C+E and resi 98+153+183+190+194+225+226")
cmd.select("fusion_peptide", "chain B+D+F and resi 1-20")

cmd.color("grey80", "chain A+C+E")
cmd.color("grey50", "chain B+D+F")

cmd.show("sticks", "rbs")
cmd.color("yellow", "rbs")
cmd.set("stick_radius", 0.4, "rbs")

cmd.show("spheres", "fusion_peptide and name CA")
cmd.set("sphere_scale", 0.7, "fusion_peptide and name CA")
cmd.color("firebrick", "fusion_peptide")

cmd.orient("all")
cmd.turn("y", -20)
cmd.png(f"{output_dir}/ha_functional_sites.png", width=1400, height=1050, dpi=150)
print("2. Rendered ha_functional_sites.png")

# Render 3: Secondary Structure View
cmd.hide("sticks", "all")
cmd.hide("spheres", "all")
cmd.color("firebrick", "ss h")   # Alpha helices
cmd.color("brightorange", "ss s") # Beta sheets
cmd.color("teal", "ss l+''")      # Loops
cmd.orient("all")
cmd.turn("x", 15)
cmd.png(f"{output_dir}/ha_secondary_structure.png", width=1400, height=1050, dpi=150)
print("3. Rendered ha_secondary_structure.png")

# Save complete session file for PyMOL
session_file = f"{output_dir}/h1n1_hemagglutinin.pse"
cmd.save(session_file)
print(f"Saved PyMOL session file to: {session_file}")

cmd.quit()
