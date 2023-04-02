# -*- mode: python ; coding: utf-8 -*-
from version import version
import platform

#
# Parameters
#
if platform.system() == 'Windows':
    onefile = True
else:
    onefile = False
block_cipher = None

app_name = 'Causal_relationships_in_school'

#
# Main spec file elements
#
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['sklearn.metrics._pairwise_distances_reduction._datasets_pair',
                   'sklearn.metrics._pairwise_distances_reduction._middle_term_computer',
                   'win32api',
                   ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries if onefile else [],
    a.zipfiles if onefile else [],
    a.datas if onefile else [],
    exclude_binaries=not onefile,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_file.txt',
)
bundle_obj = exe

if not onefile:
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name=app_name,
    )
    bundle_obj = coll

app = BUNDLE(
    bundle_obj,
    name=app_name + '.app',
    bundle_identifier="app.ariollex.causal_relationships_in_school",
    info_plist={
        'CFBundleShortVersionString': version,
    }
)
