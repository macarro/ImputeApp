# -*- mode: python ; coding: utf-8 -*-

import os

spec_root = os.path.abspath(SPECPATH)


block_cipher = None


a = Analysis(['ImputeApp.py'],
             pathex=[spec_root],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn', 'sklearn.utils._cython_blas', 'sklearn.neighbors._typedefs'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ImputeApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='ImputeApp.app',
             icon='./resources/ImputeApp.icns',
             bundle_identifier='com.imputeapp',
             info_plist={
                'CFBundleShortVersionString': '0.1.0'
             })
