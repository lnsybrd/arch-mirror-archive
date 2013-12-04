pkgver=2016.02.13
pkgname=(arch-mirror-archive)
pkgrel=1
pkgdesc='Arch mirror archive'
arch=('any')
url='https://github.com/lnsybrd/arch-mirror-archive'
license=('MIT')
depends=('python2'
         'btrfs-progs')
makedepends=('python2'
             'python2-setuptools'
             'python2-virtualenv')
provides=('arch-mirror-archive')

build() {
    # Build the virtual env
    virtualenv2 --no-site-packages --always-copy $pkgname
}

package() {
    # Virtual env
    source ${pkgname}/bin/activate

    # Do the install
    cd ${startdir}
    python2 setup.py install

    install -d "${pkgdir}/opt/${pkgname}"
    find ${srcdir}/${pkgname}/bin -type f -exec awk '/^#!.*python/{print FILENAME} {nextfile}' {} + \
        | xargs sed -i "s#!.*/bin#!/opt/${pkgname}/bin#"

    cp -r --no-preserve=ownership ${srcdir}/${pkgname}/* "${pkgdir}/opt/${pkgname}/"

    # Remove the ability to activate the venv in the package
    rm -f ${pkgdir}/opt/${pkgname}/bin/activate*

    # Remove the include directory
    rm -Rf ${pkgdir}/opt/${pkgname}/include
}

# vim:set ts=4 sw=4 et:
