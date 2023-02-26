# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
#    datas=[('languages/*', 'languages'), ('configuration', '.')],
    hiddenimports=['sklearn.metrics._pairwise_distances_reduction._datasets_pair', 'sklearn.metrics._pairwise_distances_reduction._middle_term_computer'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Causal relationships in school',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Causal relationships in school'
)

app = BUNDLE(
    coll,
    name='Causal_relationships_in_school.app',
    icon=None,
    bundle_identifier='com.ariollex.causal_relationships_in_school',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSRequiresAquaSystemAppearance': False,
        'CFBundleShortVersionString': 0.3,
    }
)