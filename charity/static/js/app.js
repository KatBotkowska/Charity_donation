document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;


            console.log(this.currentStep);

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });
            if (this.currentStep == 3) {
                let selected_categories = [];
                let checked_cat = $('input[name="categories"]:checked');
                if (checked_cat.length > 0) {
                    checked_cat.each(function () {
                        selected_categories.push($(this).val());
                    });
                }
                let organizations = $('input[name="institution"]');
                let displayed = 0;
                organizations.each(function () {
                    /*data - categories for organization*/
                    let data = Object.keys($(this).data()); /*pokaże klucze w datasecie dla danej organizacji)*/
                    if (selected_categories.every(r => data.includes(r))) {
                        $(this).parent().parent().show();
                        displayed++;
                    }

                });
                if (displayed == 0) {
                    $('div[data-step="3"] h3').text('W naszej bazie nie znależliśmy instytucji, ' +
                        'która jest w stanie odebrać wszystkie rzeczy. Zmień kategorie rzeczy do oddania ' +
                        'i spróbuj jeszcze raz.');
                    $('div[data-step="3"] button').eq(1).hide();
                } else {
                    $('div[data-step="3"] h3').text('Wybierz organizacje, której chcesz pomóc: ');
                    $('div[data-step="3"] button').eq(1).show();
                }
            }

            if (this.currentStep == 5) {
                /*co*/
                let bags = $('input[name="quantity"]').val();
                let selected_categories = [];
                let checked_cat = $('input[name="categories"]:checked');
                if (checked_cat.length > 0) {
                    checked_cat.each(function () {
                        selected_categories.push($(this).next().next().text());
                    });
                }
                $('.summary--text').eq(0).text('worki szt: ' + bags + ' a w nich: ' + selected_categories);

                /*dla kogo*/
                let checked_organization = $('input[name="institution"]:checked').next().next().text();

                $('.summary--text').eq(1).text('dla: ' + checked_organization);
                /*dane adresowe i czas*/
                let li = $('.summary li');
                li.eq(2).text($('input[name="address"]').val());
                li.eq(3).text($('input[name="city"]').val());
                li.eq(4).text($('input[name="zip_code"]').val());
                li.eq(5).text($('input[name="phone_number"]').val());
                li.eq(6).text($('input[name="pick_up_date"]').val());
                li.eq(7).text($('input[name="pick_up_time"]').val());
                let more_info = $('input[name="pick_up_comment"]')
                if (more_info.val() !== "") {
                    li.eq(8).text($('input[name="pick_up_comment"]').val());
                }
            }
            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            if (this.currentStep !== 5) {
                e.preventDefault();
                this.currentStep++;
                this.updateForm();
            }
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});