!function(e) {
    "use strict";
    var a = e(window);
    a.on("load", function() {
        var n = e(document)
          , t = e("html, body")
          , o = e(".loader-container")
          , i = e(".skillbar")
          , r = e(".header-menu-wrapper")
          , s = e("#back-to-top")
          , l = e(".card-carousel")
          , d = e(".client-logo")
          , c = e(".testimonial-carousel")
          , p = e(".testimonial-carousel-2")
          , u = e(".gallery-carousel")
          , g = e(".video-popup-btn")
          , m = e('input[name="daterange"]')
          , h = e(".user-chosen-select")
          , v = e(".team-carousel")
          , f = e(".popular-job-carousel")
          , b = e(".circlechart")
          , H = e(".user-text-editor")
          , y = e(".user-text-editor-2")
          , w = e(".user-text-editor-3")
          , C = e(".user-text-editor-4")
          , k = e(".emoji-picker");
        e(o).delay("500").fadeOut(2e3),
        n.on("click", ".side-menu-wrap .side-menu-ul>li>a .btn-toggle", function() {
            return e(this).closest("li").siblings().removeClass("active").find(".dropdown-menu-item").slideUp(200),
            e(this).closest("li").toggleClass("active").find(".dropdown-menu-item").slideToggle(200),
            !1
        }),
        n.on("click", ".logo-right-content .side-menu-open", function() {
            e(".side-nav-container").toggleClass("active")
        }),
        n.on("click", ".dashboard-nav-trigger-btn", function() {
            e(".dashboard-nav-container").addClass("active")
        }),
        n.on("click", ".user-menu-open", function() {
            e(".user-nav-container").addClass("active")
        }),
        n.on("click", ".humburger-menu .side-menu-close", function() {
            e(".side-nav-container, .dashboard-nav-container, .user-nav-container").removeClass("active")
        }),
        e(i).each(function() {
            e(this).find(".skill-item").animate({
                width: e(this).attr("data-percent")
            }, 3e3)
        }),
        a.on("scroll", function() {
            a.scrollTop() > 0 ? e(r).addClass("header-fixed") : e(r).removeClass("header-fixed"),
            a.scrollTop() > 500 ? e(s).addClass("btn-active") : e(s).removeClass("btn-active")
        }),
        n.on("click", "#back-to-top", function() {
            return e(t).animate({
                scrollTop: 0
            }, 800),
            !1
        }),
        e(l).length && e(l).owlCarousel({
            loop: !0,
            items: 2,
            nav: !1,
            dots: !1,
            autoplay: !0,
            smartSpeed: 500,
            margin: 30,
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                }
            }
        }),
        e(d).length && e(d).owlCarousel({
            loop: !0,
            items: 6,
            nav: !1,
            dots: !1,
            smartSpeed: 700,
            autoplay: !0,
            responsive: {
                0: {
                    items: 1
                },
                425: {
                    items: 2
                },
                480: {
                    items: 2
                },
                767: {
                    items: 4
                },
                992: {
                    items: 6
                }
            }
        }),
        e(c).length && e(c).owlCarousel({
            loop: !0,
            items: 3,
            nav: !1,
            dots: !0,
            smartSpeed: 700,
            autoplay: !1,
            margin: 30,
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                992: {
                    items: 3
                }
            }
        }),
        e(p).length && e(p).owlCarousel({
            loop: !0,
            items: 5,
            nav: !1,
            dots: !0,
            smartSpeed: 700,
            autoplay: !1,
            margin: 30,
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 2
                },
                991: {
                    items: 3
                },
                992: {
                    items: 4
                },
                1200: {
                    items: 5
                }
            }
        }),
        e(u).length && e(u).owlCarousel({
            loop: !0,
            items: 1,
            nav: !0,
            dots: !0,
            smartSpeed: 700,
            autoplay: !1,
            dotsData: !0,
            navText: ['<i class="la la-chevron-left"></i>', '<i class="la la-chevron-right"></i>']
        }),
        e(g).length && e(g).magnificPopup({
            type: "video"
        }),
        e(m).length && e(m).daterangepicker({
            opens: "right",
            singleDatePicker: !0
        }),
        n.on("click", ".input-number-increment", function() {
            var a = e(this).parents(".input-number-group").find(".input-number")
              , n = parseInt(a.val(), 10);
            a.val(n + 1)
        }),
        n.on("click", ".input-number-decrement", function() {
            var a = e(this).parents(".input-number-group").find(".input-number")
              , n = parseInt(a.val(), 10);
            a.val(n - 1)
        }),
        e("#slider-range").length && e("#slider-range").slider({
            range: !0,
            min: 0,
            max: 500,
            values: [50, 290],
            slide: function(a, n) {
                e("#amount").val("$" + n.values[0] + " - $" + n.values[1])
            }
        }),
        e("#amount").val("$" + e("#slider-range").slider("values", 0) + " - $" + e("#slider-range").slider("values", 1)),
        e(h).length && e(h).chosen({
            no_results_text: "Oops, nothing found!",
            allow_single_deselect: !0
        }),
        e(h).on("chosen:showing_dropdown", function(n, t) {
            var o = e(n.target).next(".chosen-container")
              , i = o.find(".chosen-drop");
            i.offset().top - a.scrollTop() + i.height() > a.height() && o.addClass("chosen-drop-up")
        }),
        e(h).on("chosen:hiding_dropdown", function(a, n) {
            e(a.target).next(".chosen-container").removeClass("chosen-drop-up")
        }),
        e(v).length && e(v).owlCarousel({
            loop: !0,
            items: 3,
            nav: !0,
            dots: !0,
            smartSpeed: 500,
            autoplay: !1,
            margin: 30,
            navText: ["<i class='la la-angle-left'></i>", "<i class='la la-angle-right'></i>"],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                991: {
                    items: 2
                },
                992: {
                    items: 3
                }
            }
        }),
        e(f).length && e(f).owlCarousel({
            loop: !0,
            items: 1,
            nav: !1,
            dots: !1,
            autoplay: !0
        }),
        e(b).length && e(b).circlechart(),
        e('[data-toggle="tooltip"]').tooltip(),
        e("#map").length && initMap("map", 40.717499, -74.044113, "images/map-marker.png"),
        e(H).length && e(H).jqte({
            placeholder: "Write your job description",
            formats: [["p", "Paragraph"], ["h1", "Heading 1"], ["h2", "Heading 2"], ["h3", "Heading 3"], ["h4", "Heading 4"], ["h5", "Heading 5"], ["h6", "Heading 6"], ["pre", "Preformatted"]]
        }),
        e(y).length && e(y).jqte({
            placeholder: "Briefly describe about your company",
            formats: [["p", "Paragraph"], ["h1", "Heading 1"], ["h2", "Heading 2"], ["h3", "Heading 3"], ["h4", "Heading 4"], ["h5", "Heading 5"], ["h6", "Heading 6"], ["pre", "Preformatted"]]
        }),
        e(w).length && e(w).jqte({
            placeholder: "Enter long description for your online resume",
            formats: [["p", "Paragraph"], ["h1", "Heading 1"], ["h2", "Heading 2"], ["h3", "Heading 3"], ["h4", "Heading 4"], ["h5", "Heading 5"], ["h6", "Heading 6"], ["pre", "Preformatted"]]
        }),
        e(C).length && e(C).jqte({
            placeholder: "Briefly describe about your company where you worked before",
            formats: [["p", "Paragraph"], ["h1", "Heading 1"], ["h2", "Heading 2"], ["h3", "Heading 3"], ["h4", "Heading 4"], ["h5", "Heading 5"], ["h6", "Heading 6"], ["pre", "Preformatted"]]
        }),
        e(k).length && e(k).emojioneArea({
            pickerPosition: "top"
        })
    })
}(jQuery);
