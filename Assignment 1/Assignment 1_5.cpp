(use debug
     foof-loop
     lolevel
     srfi-1
     srfi-8
     srfi-13
     srfi-69
     vector-lib)

(define (simulate environment)
  (loop ((while (environment)))))

(define (compose-environments . environments)
  (lambda ()
    (every identity (map (lambda (environment)
                           (environment))
                         environments))))

(define (make-performance-measuring-environment
         measure-performance
         score-update!)
  (lambda () (score-update! (measure-performance))))

(define (make-step-limited-environment steps)
  (let ((current-step 0))
    (lambda ()
      (set! current-step (+ current-step 1))
      (< current-step steps))))

;;; What about pairs of objects and optional display things.
(define make-debug-environment
  (case-lambda
   ((object) (make-debug-environment object pp))
   ((object display)
    (lambda () (display object)))))

(define (vacuum-world-display world)
  (pp
   (vector-append '#(world)
                  (vector-map
                   (lambda (i clean?)
                     (if clean? 'clean 'dirty))
                   world))))

(define clean #t)
(define clean? identity)

(define dirty #f)
(define dirty? (complement clean?))

(define left 0)
(define left? zero?)

(define right 1)
(define right? (complement zero?))

(define make-vacuum-world vector)

(define vacuum-world-location vector-ref)

(define vacuum-world-location-set! vector-set!)

(define-record vacuum-agent
  location
  score
  program)

(define-record-printer vacuum-agent
  (lambda (vacuum-agent output)
    (format output
            "#(agent ~a ~a)"
            (if (left? (vacuum-agent-location vacuum-agent))
                'left
                'right)
            (vacuum-agent-score vacuum-agent))))

(define (make-vacuum-environment world agent)
  (lambda ()
    (let* ((location (vacuum-agent-location agent))
           (action ((vacuum-agent-program agent)
                    location
                    (vacuum-world-location world location))))
      (case action
        ((left) (vacuum-agent-location-set! agent left))
        ((right) (vacuum-agent-location-set! agent right))
        ((suck) (vacuum-world-location-set! world location clean))
        (else (error (string-join
                      "make-vacuum-environment --"
                      "Unknown action")
                     action))))))

(define (reflex-vacuum-agent-program location clean?)
  (if clean?
      (if (left? location)
          'right
          'left)
      'suck))

(define make-reflex-vacuum-agent
  (case-lambda
   ((location)
    (make-reflex-vacuum-agent location reflex-vacuum-agent-program))
   ((location program)
    (make-vacuum-agent
     location
     0
     program))))

(define (make-vacuum-performance-measure world)
  (lambda ()
    (vector-count (lambda (i square) (clean? square)) world)))

(define (make-vacuum-score-update! agent)
  (lambda (score)
    (vacuum-agent-score-set! agent (+ (vacuum-agent-score agent)
                                      score))))

(define simulate-vacuum
  (case-lambda
   ((world agent) (simulate-vacuum world agent 1000))
   ((world agent steps)
    (simulate
     (compose-environments
      (make-step-limited-environment steps)
      (make-performance-measuring-environment
       (make-vacuum-performance-measure world)
       (make-vacuum-score-update! agent))
      (make-debug-environment agent)
      (make-debug-environment world vacuum-world-display)
      (make-vacuum-environment world agent)))
    (vacuum-agent-score agent))))

(simulate-vacuum (make-vacuum-world dirty clean)
                 (make-reflex-vacuum-agent
                  left
                  (lambda (location clean?)
                    'right))
                 10)