(use-modules
  (gnu packages)
  (gnu packages python-web)
  ((guix licenses) #:prefix license:)
  (guix build-system python)
  (guix download)
  (guix gexp)
  (guix git-download)
  (guix packages)
  (guix utils)
  (ice-9 popen)
  (ice-9 rdelim))

;; From the talk "Just build it with Guix" by Efraim Flashner
;; presented on the Guix days 2020
;; https://guix.gnu.org/en/blog/2020/online-guix-day-announce-2/
(define %source-dir (dirname (current-source-directory)))

(define %git-commit
  (read-string (open-pipe "git show HEAD | head -1 | cut -d ' ' -f2" OPEN_READ)))

(define %package-version
  (read-string (open-pipe "./build-aux/git-version-gen .tarball-version" OPEN_READ)))

(define (skip-git-and-build-artifacts file stat)
  "Skip git and build artifacts when collecting the sources."
  (let ((name (substring file (+ 1 (string-prefix-length %source-dir file)))))
    (not (or (string=? name ".git")))))

(define-public python-ruuvitag-form
  (package
    (name "python-ruuvitag-form")
    (version (git-version %package-version "HEAD" %git-commit))
    (source (local-file %source-dir
                        #:recursive? #t
                        #:select? skip-git-and-build-artifacts))
    (build-system python-build-system)
    (arguments `())
    (native-inputs `())
    (propagated-inputs `())
    (inputs
     `(("python-pycurl" ,python-pycurl)))
    (synopsis "Display information from a ruuvitag-hark server.")
    (description
     "Simple program that fetches data from a server running ruuvitag-hark
and output that to stdout in a format that other programs then can
then consume.")
    (home-page "")
    (license license:gpl3+)))

python-ruuvitag-form
