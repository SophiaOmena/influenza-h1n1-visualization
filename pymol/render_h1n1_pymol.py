# /// script
# requires-python = ">=3.10, <3.13"
# dependencies = [
#     "pymol-open-source-whl",
# ]
# ///

import os
import sys

# Set environment variable for headless OSMesa rendering
os.environ["PYOPENGL_PLATFORM"] = "osmesa"

import pymol
pymol.pymol_argv = ["pymol", "-cq"]
pymol.finish_launching()

from pymol import cmd, util

structure_file = "/Users/sophiadeomena/.gemini/antigravity/brain/0784b279-2fc2-4198-905d-f807d5f78ba2/1RU7/pdb_00001ru7.cif"
output_dir = "/Users/sophiadeomena/.gemini/antigravity/brain/0784b279-2fc2-4198-905d-f807d5f78ba2/pymol_output"
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(structure_file):
    print(f"Error: structure file not found: {structure_file}", file=sys.stderr)
    cmd.quit()
    sys.exit(1)

cmd.load(structure_file, "ha_h1n1")
atom_count = cmd.count_atoms("all")
print(f"Loaded {atom_count} atoms from 1RU7.")
if atom_count == 0:
    print("Error: 0 atoms loaded", file=sys.stderr)
    cmd.quit()
    sys.exit(1)

# PyMOL settings for publication-quality rendering
cmd.set("ray_opaque_background", 1)
cmd.bg_color("black")
cmd.set("antialias", 2)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_highlight_color", "grey50")
cmd.set("depth_cue", 1)
cmd.set("fog_start", 0.45)
cmd.set("specular", 0.4)
cmd.set("light_count", 3)
cmd.set("ambient", 0.25)

# Remove solvent water molecules
cmd.remove("solvent")

# --- Render 1: Multi-chain Cartoon with HA1 (heads) and HA2 (stalks) ---
# Chains A, C, E are HA1; Chains B, D, F are HA2
cmd.show_as("cartoon", "all")
cmd.color("cyan", "chain A+C+E")
cmd.color("teal", "chain A")
cmd.color("deepteal", "chain C")
cmd.color("aquamarine", "chain E")

cmd.color("marine", "chain B+D+F")
cmd.color("blue", "chain B")
cmd.color("slate", "chain D")
cmd.color("deepblue", "chain F")

cmd.orient("all")
cmd.turn("y", 30)

cmd.png(f"{output_dir}/ha_trimer_cartoon.png", width=1600, height=1200, dpi=200)
print(f"Rendered: {output_dir}/ha_trimer_cartoon.png")

# --- Render 2: Functional Sites (Receptor Binding Sites & Fusion Peptides) ---
# Sialic acid receptor binding pocket (around resi 185-195, 224-228 in HA1)
cmd.select("rbs", "chain A+C+E and resi 98+153+183+190+194+225+226")
cmd.select("fusion_peptide", "chain B+D+F and resi 1-20")

# Color background
cmd.color("grey85", "chain A+C+E")
cmd.color("grey65", "chain B+D+F")

# Highlight receptor binding pocket
cmd.show("sticks", "rbs")
cmd.color("brightorange", "rbs")
cmd.set("stick_radius", 0.35, "rbs")

# Highlight fusion peptides in red
cmd.show("sticks", "fusion_peptide")
cmd.color("firebrick", "fusion_peptide")
cmd.set("stick_radius", 0.35, "fusion_peptide")

# Semi-transparent surface to appreciate the 3D molecular envelope
cmd.show("surface", "all")
cmd.set("transparency", 0.55, "all")
cmd.set("surface_color", "grey90", "all")

cmd.png(f"{output_dir}/ha_functional_sites.png", width=1600, height=1200, dpi=200)
print(f"Rendered: {output_dir}/ha_functional_sites.png")

# --- Render 3: Close-up on the Receptor Binding Pocket ---
cmd.hide("surface", "all")
cmd.zoom("rbs and chain A", buffer=8.0)
cmd.show("surface", "chain A and (rbs expand 6.0)")
cmd.set("transparency", 0.4, "chain A and (rbs expand 6.0)")
cmd.set("surface_color", "yelloworange", "chain A and (rbs expand 6.0)")
cmd.png(f"{output_dir}/ha_rbs_closeup.png", width=1600, height=1200, dpi=200)
print(f"Rendered: {output_dir}/ha_rbs_closeup.png")

# --- Save PyMOL Session (.pse) ---
session_path = f"{output_dir}/ha_h1n1_session.pse"
cmd.save(session_path)
print(f"Saved PyMOL session: {session_path}")

cmd.quit()
print("PyMOL script completed successfully.")
