pkgver=`date +%Y.%m.%d`
pkgrel=`date +%H.%M`
pkgname=(arch-mirror-archive)
pkgdesc='Arch mirror archive'
arch=('any')
url='https://github.com/lnsybrd/arch-mirror-archive'
license=('MIT')
depends=('python'
         'btrfs-progs')
makedepends=('python'
             'python-setuptools'
             'python-virtualenv')
provides=('arch-mirror-archive')
prefix=opt

build() {
    # Build the virtual env
    virtualenv \
        --no-site-packages \
        --always-copy \
        ${pkgname}

    # Turn on the virtual env
    source ${pkgname}/bin/activate

    # Do the install
    pushd ${startdir}
    ./setup.py install
    popd

    # Remove pip and friends from the virtual env
    pip list --format=columns
    pip uninstall --yes setuptools
    pip uninstall --yes wheel
    pip uninstall --yes pip

    # Make the virtual env relocatable
    virtualenv \
        --relocatable \
        ${srcdir}/${pkgname}
}

package() {
    # Install files into pkg directory
    install -d ${pkgdir}/${prefix}/${pkgname}
    cp -r --no-preserve=ownership ${srcdir}/${pkgname}/* ${pkgdir}/${prefix}/${pkgname}/

    # Remove the ability to activate the venv in the package
    rm -f ${pkgdir}/${prefix}/${pkgname}/bin/activate
    rm -f ${pkgdir}/${prefix}/${pkgname}/bin/activate.*

    # Don't make it easy to compile/link against this virtualenv
    rm -f ${pkgdir}/${prefix}/${pkgname}/bin/python-config

    # Remove the include directory
    rm -Rf ${pkgdir}/${prefix}/${pkgname}/include

    # Clean up left over stuff from pip
    rm -f ${pkgdir}/${prefix}/${pkgname}/pip-selfcheck.json
}

# vim:set ts=4 sw=4 et:
