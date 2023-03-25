# -*- mode: python ; coding: utf-8 -*-


#
# Set various parameters
#
app_version = "0.3.0"
onefile = False
block_cipher = None


#
# Main spec file elements
#
a = Analysis(['main.py'],
        binaries=[],
        datas=[],
        hiddenimports=['sklearn.metrics._pairwise_distances_reduction._datasets_pair',
                       'sklearn.metrics._pairwise_distances_reduction._middle_term_computer',
                       'win32api',
                       ],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False
    )

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)

exe = EXE(pyz,
        a.scripts,
        a.binaries if onefile else [],
        a.zipfiles if onefile else [],
        a.datas if onefile else [],
        exclude_binaries=not onefile,
        name='main',
        debug=True,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
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
            name='main',
        )
    bundle_obj = coll

app = BUNDLE(bundle_obj,
        name='main.app',
        bundle_identifier="app.ariollex",
        info_plist={
            'CFBundleShortVersionString': app_version,
        }
    )