;; The current version is very naive and blindly clears (periodically) whatever
;; buffer is currently selected (though a blank buffer is created and selected
;; initially). If you want to try it out, use an emacs session without any work
;; that could be corrupted.
;;
;; Some potential things to do:
;; - [ ] Make the buffer full screen.
;; - [ ] Allow the user to return to the previous window configuration.
;; - [ ] Allow the option of filling the visible buffer with the board.
;; - [ ] Allow the user to supply an initial configuration explicitly.
;; - [ ] Allow the user to draw an initial configuration?
;; - [ ] Create a major mode?

;; Generic functions
(defun subtract (&rest lists)
  (apply #'mapcar* #'- lists))

(defun sum (&rest lists)
  (apply #'mapcar* #'+ lists))

(defun zip (&rest lists)
  (apply #'mapcar* #'list lists))

;; Create a new game
(defvar game-of-life-update-timer)
(defvar board)

(defun new-game-of-life (&optional rows cols)
  (let ((buffer (generate-new-buffer "*game-of-life*")))
    (switch-to-buffer buffer)
    (cond ((not rows)
           (setq rows (- (window-body-height) 2))
           (setq cols (/ (- (window-body-width) 3) 2)))
          ((not cols)
           (setq cols rows)))
    (setq board (create-game-of-life-board rows cols))
    (defun local-update ()
      (setq newboard (update-game-of-life-board board))
      (cond ((equal board newboard)
             (cancel-timer game-of-life-update-timer)
             (insert "\nStable configuration!"))
            (t (setq board newboard)
               (erase-buffer)
               (draw-game-of-life-board newboard))))
    (setq game-of-life-update-timer
          (run-at-time "0 sec" 0.5
                       #'local-update))))

;; Creating a board
(defun create-game-of-life-row (cols)
  (cond ((eq cols 0) 'nil)
        (t (cons (random 2)
                 (create-game-of-life-row (- cols 1))))))

(defun create-game-of-life-board (rows cols)
  (cond ((eq rows 0) 'nil)
        (t (cons (create-game-of-life-row cols)
                 (create-game-of-life-board (- rows 1) cols)))))

;; Drawing a board
(defun draw-game-of-life-board (board)
  (defun draw-top-or-bottom (ncols)
    (insert " ")
    (insert-char ?- (+ (* 2 ncols) 1))
    (insert " "))
  (cond (board (let ((ncols (length (car board))))
                 (draw-top-or-bottom ncols)
                 (insert "\n")
                 (draw-game-of-life-board-inner board)
                 (draw-top-or-bottom ncols)))))

(defun draw-game-of-life-board-inner (board)
  (cond (board (draw-game-of-life-row (car board))
               (draw-game-of-life-board-inner (cdr board)))))

(defun draw-game-of-life-row (row)
  (cond ((not (eq row 'nil))
         (insert "| ")
         (draw-game-of-life-row-inner row)
         (insert "|")))
  (insert-char ?\n 1))

(defun draw-game-of-life-row-inner (row)
  (cond ((not (eq row 'nil))
         (cond ((eq (car row) 1) (insert "o"))
               (t (insert " ")))
         (insert " ")
         (draw-game-of-life-row-inner (cdr row)))))

;; Update a board
(defun count-neighbors-in-row (row)
  (sum row
       (append (cdr row) '(0))
       (cons 0 (reverse (cdr (reverse row))))))

(defun count-neighbors (board)
  (let ((row-nbrs (mapcar #'count-neighbors-in-row board))
        (row-length (length (car board))))
    (mapcar #'(lambda (lists) (apply #'sum lists))
            (zip row-nbrs
                 (append (cdr row-nbrs)
                         (list (make-list row-length 0)))
                 (cons (make-list row-length 0)
                       (reverse (cdr (reverse row-nbrs))))
                 (mapcar #'subtract board)))))

(defun update-game-of-life-cell (value nbrs)
  (if (eq value 0)
      (if (eq nbrs 3) 1 0)
    (if (or (eq nbrs 2) (eq nbrs 3))
        1 0)))

(defun update-game-of-life-board (board)
  (let ((nbrs (count-neighbors board)))
    (mapcar #'(lambda (row)
                (mapcar #'(lambda (pair)
                            (apply #'update-game-of-life-cell pair))
                        row))
            (mapcar #'(lambda (lists)
                        (apply #'zip lists))
                    (zip board nbrs)))))

;; Testing

;; (defun junk-func ()
;;   (interactive)
;;   (cancel-timer game-of-life-update-timer))
;; (global-set-key (kbd "C-c C-t") 'junk-func)
;; (new-game-of-life)


;; (setq tmp '((0 0 0 1 0) (0 1 0 0 1) (0 0 1 1 0) (1 1 0 0 1) (1 1 0 0 0)))
;; (draw-game-of-life-board tmp)
;;
;; (setq jnk (update-game-of-life-board tmp))
;; (draw-game-of-life-board jnk)
;;
;; (setq jnk (update-game-of-life-board jnk))
;; (draw-game-of-life-board jnk)

;; How the board should look:
;;    ---------------------
;;   |         o       o   |
;;   | o           o   o o |
;;   | o o   o o   o   o   |
;;   | o       o   o o     |
;;   | o         o o   o   |
;;   | o o   o o o         |
;;   | o         o   o   o |
;;   |     o       o o   o |
;;   |   o o   o     o o o |
;;   |   o o   o   o       |
;;    ---------------------
