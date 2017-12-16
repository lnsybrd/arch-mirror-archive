pkgver=r6.53688af
pkgver() {
    cd "${startdir}"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}
pkgrel=1
pkgname=(btrsync)
pkgdesc='Btrfs + rsync sync tool'
arch=('any')
url='https://github.com/zeroxoneb/btrsync'
license=('MIT')
depends=('python'
         'btrfs-progs')
makedepends=('python'
             'python-setuptools'
             'python-virtualenv')
provides=('btrsync')
prefix=opt

# Source is with us
source=()
md5sums=()

prepare() {
    mkdir -p ${srcdir}/${pkgname}
    cp -a ${startdir}/setup.py ${srcdir}/${pkgname}
    cp -a ${startdir}/${pkgname} ${srcdir}/${pkgname}
    cp -a ${startdir}/requirements ${srcdir}/${pkgname}
    cp -a ${startdir}/README.rst ${srcdir}/${pkgname}
}    

build() {
    # Build the virtual env
    virtualenv \
        --always-copy \
        venv/${pkgname}

        # --no-site-packages \

    # Turn on the virtual env
    source venv/${pkgname}/bin/activate

    # Do the install
    pushd ${srcdir}/${pkgname} 1> /dev/null
    ./setup.py install
    popd 1> /dev/null

    # Remove pip and friends from the virtual env
    pip list --format=columns
    pip uninstall --yes setuptools
    pip uninstall --yes wheel
    pip uninstall --yes pip

    # Make the virtual env relocatable
    virtualenv \
        --relocatable \
        ${srcdir}/venv/${pkgname}
}

package() {
    # Install files into pkg directory
    install -d ${pkgdir}/${prefix}/${pkgname}
    cp -r --no-preserve=ownership ${srcdir}/venv/${pkgname}/* ${pkgdir}/${prefix}/${pkgname}/

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
