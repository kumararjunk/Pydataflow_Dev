var App = function () {
    var $ = jQuery;
    function handleSliders() {
        $( '#elastislide' ).elastislide( {
				minItems : 2
			} );

		$('#clients-flexslider').flexslider({
			animation: "slide",
			easing: "swing",
			animationLoop: true,
			itemWidth: 1,
			itemMargin: 1,
			minItems: 2,
			maxItems: 9,
			controlNav: false,
			directionNav: false,
			move: 2
		});
		
		$('#photo-flexslider').flexslider({
			animation: "slide",
			controlNav: false,
			animationLoop: false,
			itemWidth: 80,
			itemMargin: 0
		});	
		
		$('#testimonal_carousel').collapse({
			toggle: false
		});
    }

    function handleFancybox() {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
            $('.img-modal').click(function(event) {
                $("#img-in-modal").attr("src", $(this).attr('href'));
                $('#myModal').modal('show');
                return false;
            });
        } else {
            $(".fancybox-button").fancybox({
            groupAttr: 'data-rel',
            prevEffect: 'none',
            nextEffect: 'none',
            closeBtn: true,
            helpers: {
                title: {
                    type: 'inside'
                    }
                }
            });
        }
    }

    function handleIEFixes() {
        //fix html5 placeholder attribute for ie7 & ie8
        if ($.browser.msie && $.browser.version.substr(0, 1) < 9) { // ie7&ie8
            $('input[placeholder], textarea[placeholder]').each(function () {
                var input = $(this);

                $(input).val(input.attr('placeholder'));

                $(input).focus(function () {
                    if (input.val() == input.attr('placeholder')) {
                        input.val('');
                    }
                });

                $(input).blur(function () {
                    if (input.val() == '' || input.val() == input.attr('placeholder')) {
                        input.val(input.attr('placeholder'));
                    }
                });
            });
        }
    }

    function handleBootstrap() {
        /*$('.carousel').carousel({
            interval: 15000,
            pause: 'hover'
        });*/
        $('.tooltips').tooltip({container: 'body', html: true});
        $('.popovers').popover();
    }

/*
    function handleMisc() {
        $('.top').click(function () {
            jQuery('html,body').animate({
                scrollTop: jQuery('body').offset().top
            }, 400);
        }); //move to top navigator
    }*/

    function handleSearch() {
	
        $('.search').click(function () {
          if (typeof $.cseLoaded == 'undefined') {

            var clearLoaddingText = function() {
                $('#googleCseWrapper').html('');
            }

            var myCallback = function() {
              if (document.readyState == 'complete') { 

                  clearLoaddingText();
                // Document is ready when CSE element is initialized.
                // Render an element with both search box and search results in div with id 'test'.
               
                google.search.cse.element.render(
                    {
                      div: "googleCseWrapper",
                      tag: 'search'
                     });
              } else {
                // Document is not ready yet, when CSE element is initialized.
                google.setOnLoadCallback(function() {
                    clearLoaddingText();
                   // Render an element with both search box and search results in div with id 'test'.
                    google.search.cse.element.render(
                        {
                          div: "googleCseWrapper",
                          tag: 'search'
                        });
                }, true);
              }
            };

            // Insert it before the CSE code snippet so that cse.js can take the script
            // parameters, like parsetags, callbacks.
            window.__gcse = {
              parsetags: 'explicit',
              callback: myCallback
            };

            (function() {
              var cx = '003871380498861032811:gazqf18r6iw'; // Insert your own Custom Search engine ID here
              var gcse = document.createElement('script'); gcse.type = 'text/javascript';
              gcse.async = true;
              gcse.src = (document.location.protocol == 'https' ? 'https:' : 'http:') +
                  '//www.google.com/cse/cse.js?cx=' + cx;
              var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(gcse, s);
            })();

            $.cseLoaded = true;

          }

			if($('.search-btn').hasClass('icon-search')){
				$('.search-open').fadeIn(200);
				$('.search-btn').removeClass('icon-search');
				$('.search-btn').addClass('icon-remove');
			} else {
				$('.search-open').fadeOut(200);
				$('.search-btn').addClass('icon-search');
				$('.search-btn').removeClass('icon-remove');
			}	
        }); 
    }

    function isMail(mail) {
        return(new RegExp(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/).test(mail));
    }

    function handleContactForm () {
        $('#contactUsForm').submit(function(){
            emailAddress = $('#emailAddress').val();
            messageTitle = $('#messageTitle').val();
            message = $('#message').val();

            if (!emailAddress) {
                alert('Please enter your email address.');
                return false;
            } else if (messageTitle.length > 100){
                alert('Your message title cannot be longer than 100 characters.');
                return false;
            } else if (message.length < 5) {
                alert('Your message cannot be shorter than 5 characters.');
                return false;		
            } else if (message.length > 1000) {
                alert('Your message cannot be longer than 1000 characters.');
                return false;
            } else if (!isMail(emailAddress)) {
                alert('Your email address is not valid.');
                return false;
            }
        }); 
    }

    function disableToggleLink() {
        $('a.accordion-toggle').click(function(){
            if ($(this).parent().next().is(':visible')) {
               $(this).parent().next().slideUp(); 
            } else {
                $(this).parent().next().slideDown();
            }
            return false;
        });

        $('a#extendCollapseAll').click(function(){
            if ($(this).text() == '- Hide all answers') {
                $(this).text('+ Show all answers');
                $('.accordion-body').slideUp();
            } else {
                $(this).text('- Hide all answers');
                $('.accordion-body').slideDown();
            }
            return false;
        });
    }

   function handleCronJobGenerator(){
        $('select[name="selectMinutes[]"], select[name="selectHours[]"], select[name="selectDays[]"], select[name="selectMonths[]"], select[name="selectWeekdays[]"]').on('click', function(){
            $(this).parent().parent().find('input:radio').prop('checked', true);
        });
        
        $('#cronJobGenerator').submit(function(){
            var minutes = $("input:radio[name='minutes']:checked").val();
            if (minutes == 'select') {
                var selectMinutes = $('select[name="selectMinutes[]"]').val();
                if (!selectMinutes) {
                    alert('Please choose at least one entry in minute field.');
                    return false;
                }			
            }
            var hours = $("input:radio[name='hours']:checked").val();
            if (hours == 'select') {
                var selectHours = $('select[name="selectHours[]"]').val();
                if (!selectHours) {
                    alert('Please choose at least one entry in hour field.');
                    return false;
                }			
            }
            var days = $("input:radio[name='days']:checked").val();
            if (days == 'select') {
                var selectDays = $('select[name="selectDays[]"]').val();
                if (!selectDays) {
                    alert('Please choose at least one entry in day field.');
                    return false;
                }			
            }
            var months = $("input:radio[name='months']:checked").val();
            if (months == 'select') {
                var selectMonths = $('select[name="selectMonths[]"]').val();
                if (!selectMonths) {
                    alert('Please choose at least one entry in month field.');
                    return false;
                }			
            }
            var weekdays = $("input:radio[name='weekdays']:checked").val();
            if (weekdays == 'select') {
                var selectWeekdays = $('select[name="selectWeekdays[]"]').val();
                if (!selectWeekdays) {
                    alert('Please choose at least one entry in weekday field.');
                    return false;
                }			
            }

            var command = $("input[name='command']").val();
            if (!command) {
                alert('Please enter a command.');
                return false;
            }

            var output = $("input:radio[name='output']:checked").val();
            if (output == '2') {
                var filePath = $("input[name='filePath']").val();
                if (!filePath) {
                    alert('Please enter a file path for saving output.');
                    return false;
                }
            }
            if (output == '3') {
                var outputEmail = $("input[name='outputEmail']").val();
                if (!outputEmail) {
                    alert('Please enter an Email address.');
                    return false;
                } else {
                    if (!isMail(outputEmail)) {
                        alert('Please enter a valid Email address.');
                        return false;
                    }
                }
            }            
        });    
    }

    function handleRunTimePredictor () {
        $('#cronJobPredict').submit(function(){
            cronExpression = $('#cronExpression').val();
            if (!cronExpression) {
                alert('Please enter a cron expression.');
                return false;
            }
        });
    }

    var quickRegisterFormFieldsValid = true;
    function checkUsernameAvailability(username, email) {
         /*$.get('/user/ajaxavailability/username/' + username + '/email/' + email,
            function(data){
                if (data == '0') {
                   alert('The username is already taken, please choose another one.');
                   quickRegisterFormFieldsValid = false;
                   return false;
                }
            }
        );*/

        $.ajax({
             url:    '/user/ajaxavailability/username/' + username + '/email/' + email,
             success: function(data){
                        if (data == '0') {
                           alert('The username is already taken, please choose another one.');
                           quickRegisterFormFieldsValid = false;
                           return false;
                        }
                    },
             async:   false
        });  
    }

    function validateUsername($username, $emailAddress) {
        var length = $username.val().length;
        if (length == 0) {
            alert('Please enter a username.');
            quickRegisterFormFieldsValid = false;
        } else {
            if (! /^[a-zA-Z0-9_]+$/.test($username.val())) {
                alert('Only letters, numbers and underscore are allowed in username.');
                quickRegisterFormFieldsValid = false;
                return false;
            }
            if ((length < 4) || (length > 20)) {
                alert('Username\'s length should be within 4 - 20 chars.');
                quickRegisterFormFieldsValid = false;
                return false;
            }
            checkUsernameAvailability($username.val(), $emailAddress.val());
        } 
    }

    function checkEmailAvailability(email) {
         /*$.get('/user/ajaxavailability/email/' + email,
            function(data){
                if (data == '0') {
                   alert('The Email address is already taken, please use another one.');
                   quickRegisterFormFieldsValid = false;
                   return false;
                }
            }
        );*/
        $.ajax({
             url:    '/user/ajaxavailability/email/' + email,
             success: function(data){
                        if (data == '0') {
                           alert('The Email address is already taken, please use another one.');
                           quickRegisterFormFieldsValid = false;
                           return false;
                        }
                    },
             async:   false
        });  
    }

    function validateEmail($emailAddress) {
        var length = $emailAddress.val().length;
        if (length == 0) {
            alert('Please enter an Email address.');
            quickRegisterFormFieldsValid = false;
        } else {
            if (!isMail($emailAddress.val())) {
                alert('Please enter a valid Email address.');
                quickRegisterFormFieldsValid = false;
                return false;
            }
            checkEmailAvailability($emailAddress.val());
        }
    }

    function validatePassword($password) {
        var length = $password.val().length;
        if (length == 0) {
            alert('Please enter a password.');
            quickRegisterFormFieldsValid = false;
        } else {
            if ((length < 6) || (length > 20)) {
                alert('Username\'s length should be within 6 - 20 chars.');
                quickRegisterFormFieldsValid = false;
                return false;
            }
        }
    }

    function handleQuickRegister() {
        /*
        $('.quick-reg input[name="username"]').blur(function(){
            return validateUsername($(this), $('.quick-reg input[name="emailAddress"]').eq(0));
        }).change(function(){quickRegisterFormFieldsValid = true;});

        $('.quick-reg input[name="emailAddress"]').blur(function(){
            return validateEmail($(this));
        }).change(function(){quickRegisterFormFieldsValid = true;});

        $('.quick-reg input[name="password"]').blur(function(){
            return validatePassword($(this));
        }).change(function(){quickRegisterFormFieldsValid = true;});*/

        // quick register
        $('.homepage-intro .quick-reg').submit(function(){
            quickRegisterFormFieldsValid = true;
            validateUsername($('.quick-reg input[name="username"]').eq(0), $('.quick-reg input[name="emailAddress"]').eq(0));
            if (!quickRegisterFormFieldsValid) {
                return false;
            }
            validateEmail($('.quick-reg input[name="emailAddress"]').eq(0));
            if (!quickRegisterFormFieldsValid) {
                return false;
            }
            validatePassword($('.quick-reg input[name="password"]').eq(0));
            if (!quickRegisterFormFieldsValid) {
                return false;
            }
        });
    }

    function handleRegister() {
        // user register form
        $('#userRegisterForm').submit(function(){
            username = $('#username').val();
            password = $('#password').val();
            //passwordConfirm = $('#passwordConfirm').val();
            emailAddress = $('#emailAddress').val();
            paymentMethod = $('input[name$="payment_method"]:checked').val();

            if (!username) {
                alert('Please enter your username.');
                return false;
            } else if (!password){
                alert('Plesae enter your password.');
                return false;
            } /*else if (!passwordConfirm) {
                alert('Please confirm your password.');
                return false;
            }*/ else if (!emailAddress) {
                alert('Please enter your email address.');
                return false;
            } else if (!isMail(emailAddress)) {
                alert('Your email address is not valid.');
                return false;
            }/* else if (password != passwordConfirm) {
                alert('Your passwords don\'t match.');
                return false;
            }*/ else if ((!$('input[name="p_plan_id"].freePlan').attr('checked')) && (!paymentMethod)) {
                alert('Please choose a payment method.');
                return false;
            }
        });
    }

    function handlePlanChange() {
         $('#planUpgradeForm').submit(function(){
            paymentMethod = $('input[name$="payment_method"]:checked').val();
            if ((!$('input[name="p_plan_id"].freePlan').attr('checked')) && (!paymentMethod)) {
                alert('Please choose a payment method.');
                return false;
            }
        });
    }

    function handlePlan() {
        $('input[name="p_plan_id"]:checked.paidPlan').parent().parent().removeClass('availablePlan').addClass('selectedPlan').end().end().next().find('i').removeClass('icon-check-empty').addClass('icon-check');
        $('input[name="p_plan_id"]:checked.freePlan').next().find('i').removeClass('icon-check-empty').addClass('icon-check');

       
        // bigger plan choosing zone
        $('.availablePlan h3').live('click', function(){
            $('.pricing input:checked').attr('checked', false);
            $(this).parent().prev().attr('checked', true);
            $('.selectedPlan').removeClass('selectedPlan').addClass('availablePlan').find('h3 i').removeClass('icon-check').addClass('icon-check-empty');
            $('input:checked').parent().removeClass('availablePlan').addClass('selectedPlan').end().next().find('h3 i').removeClass('icon-check-empty').addClass('icon-check');
            

            if ($(this).parent().parent().hasClass('freePlan')) {
                $('.extraZone').slideUp();
                $('.paymentMethodZone').slideUp();
                $('.longTermCycle'). slideUp();
                $('#updateBtn').slideUp();
                $('.antibotZone').slideDown();
            } else {
                $('.extraZone').slideDown();
                $('.paymentMethodZone').slideDown();
                $('.longTermCycle').slideDown();
                $('.antibotZone').slideUp();
                $('#updateBtn').slideDown();
            }
        });
    }

    function bootboxAlert(notice) {
        bootbox.dialog(notice, 
            [{
                "label" : "OK",
                "class" : "btn",
                "callback": function() {                    
                }
            }], 
            {
            "backdrop" : "static",
            "keyboard" : false,
            "show" : true,
            "animate" : false,
        });
    }
    function bootboxConfirm(notice) {
        bootbox.dialog(notice, 
            [{
                "label" : "Yes",
                "class" : "btn",
                "callback": function() {                    
                }
            },
            {
                "label" : "Cancel",
                "class" : "btn",
                "callback": function() {                    
                }
            }], 
            {
            "backdrop" : "static",
            "keyboard" : false,
            "show" : true,
            "animate" : false,
        });
    }

    function getSelectValue(radio)
    {
        for (var i = 0; i < radio.length; i++ ) {
            if (radio[i].checked) {
                return radio[i].value;
            }
        }    
    }

    function isValidUrl(url) {
        if (/^([a-z]([a-z]|\d|\+|-|\.)*):(\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?((\[(|(v[\da-f]{1,}\.(([a-z]|\d|-|\.|_|~)|[!\$&'\(\)\*\+,;=]|:)+))\])|((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=])*)(:\d*)?)(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*|(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)){0})(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url)) {
            return true;
        } else {
            return false;
        }
    }

    function handleCronJobSettings(rightNow) {
        // ajax create cron job form
        var cronCreateOptions = { 
            beforeSubmit: function(formData, jqForm, validateOptions) {
                var form = jqForm[0];
            },
            beforeSerialize: function(form, options) {
                var form = form[0];

                if (!form.url.value) {
                    alert('You should enter a URL.');
                    form.url.focus();
                    exitLoadingMode($('#cronJobSettingsDone'));
                    return false;
                } else if ((!isValidUrl(form.url.value)) || (form.url.value == 'http://')) {
                    alert('The URL you entered is not valid.');
                    form.url.focus();
                    exitLoadingMode($('#cronJobSettingsDone'));
                    return false;
                }

                var specifiedBy = getSelectValue(form.specifiedBy);
                if (specifiedBy == '1') {
                    if ((form.timeInterval.value < 1) || (form.timeInterval.value > 26)) {
                        alert('Please choose an interval.');
                        form.timeInterval.focus();
                        exitLoadingMode($('#cronJobSettingsDone'));
                        return false;
                    }
                }

                if (specifiedBy == '2') {
                    if (!form.cron_expression.value) {
                        alert('Please enter a cron expression.');
                        form.cron_expression.focus();
                        exitLoadingMode($('#cronJobSettingsDone'));
                        return false;
                    } else {
                        if (($.trim(form.cron_expression.value).split(' ').length - 1) != 4) {
                            alert('The cron expression you entered is invalid.');
                            form.cron_expression.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                }

                if (specifiedBy == '3') {
                    var all_mins = getSelectValue(form.all_mins);
                    if (all_mins == 2) {
                        if (!form.all_minutes_random_times.value) {
                            alert('Please enter a random time for minute field.');
                            form.all_minutes_random_times.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                        if ((isNaN(form.all_minutes_random_times.value)) || (form.all_minutes_random_times.value < 1) || (form.all_minutes_random_times.value > 60)) {
                            alert('The random time for minute field must be between 1 - 60.');
                            form.all_minutes_random_times.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                    if (all_mins == 0) {
                        if (!$(form).find('select[name="mins[]"] option:selected').length) {
                            alert('Please choose at least one minute.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }

                    var all_hours = getSelectValue(form.all_hours);
                    if (all_hours == 2) {
                        if (!form.all_hours_random_times.value) {
                            alert('Please enter a random time for hour field.');
                            form.all_hours_random_times.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                        if ((isNaN(form.all_hours_random_times.value)) || (form.all_hours_random_times.value < 1) || (form.all_hours_random_times.value > 60)) {
                            alert('The random time for hour field must be between 1 - 60.');
                            form.all_hours_random_times.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                    if (all_hours == 0) {
                        if (!$(form).find('select[name="hours[]"] option:selected').length) {
                            alert('Please choose at least one hour.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }

                    var all_days = getSelectValue(form.all_days);
                    if (all_days == 2) {
                        if (!form.all_days_random_times.value) {
                            alert('Please enter a random time for day field.');
                            form.all_days_random_times.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                        if ((isNaN(form.all_days_random_times.value)) || (form.all_days_random_times.value < 1) || (form.all_days_random_times.value > 31)) {
                            alert('The random time for day field must be between 1 - 31.');
                            form.all_days_random_times.focus();
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                    if (all_days == 0) {
                        if (!$(form).find('select[name="days[]"] option:selected').length) {
                            alert('Please choose at least one day.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                    if (all_days == 4) {
                        if (!$(form).find('select[name="days[]"] option:selected').length) {
                            alert('Please choose a day.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }

                    var all_months = getSelectValue(form.all_months);
                    if (all_months == 0) {
                        if (!$(form).find('select[name="months[]"] option:selected').length) {
                            alert('Please choose at least one month.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }

                    var all_weekdays = getSelectValue(form.all_weekdays);
                    if (all_weekdays == 0) {
                        if (!$(form).find('select[name="weekdays[]"] option:selected').length) {
                            alert('Please choose at least one weekday.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                    if ((all_weekdays == 3) || (all_weekdays == 4)) {
                        if (!$(form).find('select[name="weekdays[]"] option:selected').length) {
                            alert('Please choose a weekday.');
                            exitLoadingMode($('#cronJobSettingsDone'));
                            return false;
                        }
                    }
                }

                /*
                query = '';                
                if (form.url.value != decodeURIComponent($('#url').attr('data-url'))) {
                    if (confirm('Do you want EasyCron to test your URL first? (Recommended)')) {
                        query = '?testfirst=1';
                    }
                }*/
                url = $(form).attr('action');// + query;
                options['url'] = url;
            },
            success: function(data) {
                if (data.redirect) {
                    // redirect to login page
                    location.reload();
                }  else if (data.error) {
                    positionTopNotice(data.error, 'error');
                    exitLoadingMode($('#cronJobSettingsDone'));
                } else if (!isNaN(data)) {
                    // secceeded
                    positionTopNotice('Done. Refreshing page ...', 'success');
                    location = '/user';
                } else {
                    // failed
                    alert(data);
                    exitLoadingMode($('#cronJobSettingsDone'));
                    return false;
                }
            },
            dataType: "json",
        };

        if (typeof rightNow != 'undefined') {
            switchToLoadingMode($('#cronJobSettingsDone'));
            $('.cronJobSetting').ajaxSubmit(cronCreateOptions); 
        } else {
            $('#cronJobSettingsDone').click(function() {
                switchToLoadingMode($(this));
                $('.cronJobSetting').ajaxSubmit(cronCreateOptions); 
                // always return false to prevent standard browser submit and page navigation 
                return false; 
            });
        }
    }
    
    function enable_cron_fields(name, form, ena, mode)
    {
        var els = form.elements[name];
        var kept = false;
        //els.disabled = !ena;

        if (name == 'months[]') {
            els.disabled = !ena;
            if (mode == 0) {
                for (var j=0;j<els.options.length;j++) {
                    if (els.options[j].selected) {
                        els.options[j].selected = false;
                    }
                }
            }
        } else if (name == 'weekdays[]') {
            els.disabled = !ena;
            if (mode == 1) {

                // bind single-select
                els.onchange = function() {
                    for (var j=0;j<els.options.length;j++) {
                        if (els.options[j].value != this.value) {
                            els.options[j].selected = false;
                        }
                    }
                }
                      
                for (var j=0;j<els.options.length;j++) {
                    if (els.options[j].selected) {
                        if (!kept) {
                            kept = true;
                            continue;
                        } else {
                            els.options[j].selected = false;
                        }
                    }
                }
            } else {
                els.onchange = null;
            }
            if (mode == 0) {
                for (var j=0;j<els.options.length;j++) {
                    if (els.options[j].selected) {
                        els.options[j].selected = false;
                    }
                }
            }
        } else {
        
            for(var i=0; i<els.length; i++) {
              els[i].disabled = !ena;
                 
              if (mode == 1) {
                    // bind single-select
                    els[i].onchange = function() {
                        for (i=0; i < els.length; i++) {                        
                            if (els[i] != this) {
                                if (typeof els[i] != 'undefined') {
                                    for (var j=0;j<els[i].options.length;j++) {
                                        if (els[i].options[j].selected) {
                                            els[i].options[j].selected = false;
                                        }
                                    }
                                }
                            } else {
                                if (typeof els[i] != 'undefined') {
                                    for (var j=0;j<els[i].options.length;j++) {
                                        if (els[i].options[j].value != this.value) {
                                            els[i].options[j].selected = false;
                                        }
                                    }
                                }
                            }
                        }
                    }
                  
                    for (var j=0;j<els[i].options.length;j++) {
                        if (els[i].options[j].selected) {
                            if (!kept) {
                                kept = true;
                                continue;
                            } else {
                                els[i].options[j].selected = false;
                            }
                        }
                    }
                } else {
                    els[i].onchange = null;
                }


                if (mode == 0) {
                    if (typeof els[i] != 'undefined') {
                        for (var j=0;j<els[i].options.length;j++) {
                            if (els[i].options[j].selected) {
                                els[i].options[j].selected = false;
                            }
                        }
                    }
                }
            }
        }
    }

    function cronJobSettingsLoaded()
    {
        if ($("#cronJobSettings").find('.modal-body').text() == '{"redirect":"\\/user\\/login"}') {
            window.location = '/user/login';
        } else {

            $('#topNotice').hide();

            $('input[name="specifiedBy"]').click(function(){
                switch ($(this).val()) {
                    case '1':
                    case '2':
                        $(this).parent().parent().find('.timesAndDates').slideUp('fast');
                        break;
                    case '3':
                        $(this).parent().parent().find('.timesAndDates').slideDown('fast');
                        break;
                    default: 
                        break;
                };
            });

            $('select[name="timeInterval"]').focus(function(){
                $('input[name="specifiedBy"][value="1"]').click();
            });

            $('#cron_expression').focus(function(){
                $('input[name="specifiedBy"][value="2"]').click();
            });

            $('.timesAndDates input[type="radio"]').change(function(){
                var name = $(this).attr('data-name');
                var form = $(this).closest('form')[0];
                var ena = ($(this).attr('data-ena') == '1') ? true : false;
                var mode = $(this).attr('data-mode');
                enable_cron_fields(name, form, ena, mode);
            })

            $('input[name="all_minutes_random_times"], input[name="all_hours_random_times"], input[name="all_days_random_times"], input[name="ordinal"]').click(function(){
                $(this).parent().find('input:radio').trigger('click');//attr('checked', true);
            });
            

            // if edit view
            if ($('#editView').length) {
                // initialize the eidt form
                if (typeof cronJobSettings != 'undefined') {
                    // populate the fields
                    $('#url').val(cronJobSettings.url);

                    switch (cronJobSettings.specified_by) {
                        case '1':
                            $('input:radio[name="specifiedBy"]:nth(0)').attr('checked', true);
                            $('select[name="timeInterval"]').find('option[value="' + cronJobSettings.specified_value + '"]').attr('selected', true);
                            break;
                        case '2':
                            $('input:radio[name="specifiedBy"]:nth(1)').attr('checked',true);
                            $('input[name="cron_expression"]').val(cronJobSettings.specified_value);
                            break;
                        case '3':
                            $('input:radio[name="specifiedBy"]:nth(2)').click();
                            var specified_value = $.parseJSON(cronJobSettings.specified_value);

                            $('input:radio[name="all_mins"][value="' + specified_value.all_mins + '"]').click();
                            if (specified_value.all_mins == 2) {
                                $('input[name="all_minutes_random_times"]').val(specified_value.all_minutes_random_times);
                            } else if (specified_value.all_mins == 0) {
                                $.each(specified_value.mins, function (index, value) {
                                    $('select[name="mins[]"]').find('option[value="' + value + '"]').attr('selected', true);
                                })
                            }

                            $('input:radio[name="all_hours"][value="' + specified_value.all_hours + '"]').click();
                            if (specified_value.all_hours == 2) {
                                $('input[name="all_hours_random_times"]').val(specified_value.all_hours_random_times);
                            } else if (specified_value.all_hours == 0) {
                                $.each(specified_value.hours, function (index, value) {
                                    $('select[name="hours[]"]').find('option[value="' + value + '"]').attr('selected', true);
                                })
                            }

                            $('input:radio[name="all_days"][value="' + specified_value.all_days + '"]').click();
                            if (specified_value.all_days == 4) {
                                $('select[name="days[]"]').find('option[value="' + specified_value.days + '"]').attr('selected', true);
                            } else if (specified_value.all_days == 2) {
                                $('input[name="all_days_random_times"]').val(specified_value.all_days_random_times);
                            } else if (specified_value.all_days == 0) {
                                $.each(specified_value.days, function (index, value) {
                                    $('select[name="days[]"]').find('option[value="' + value + '"]').attr('selected', true);
                                })
                            }

                            $('input:radio[name="all_months"][value="' + specified_value.all_months + '"]').click();
                            if (specified_value.all_months == 0) {
                                $.each(specified_value.months, function (index, value) {
                                    $('select[name="months[]"]').find('option[value="' + value + '"]').attr('selected', true);
                                })
                            }

                            $('input:radio[name="all_weekdays"][value="' + specified_value.all_weekdays + '"]').click();
                            if (specified_value.all_weekdays == 3) {
                                $('select[name="weekdays[]"]').find('option[value="' + specified_value.weekdays + '"]').attr('selected', true);
                            } else if (specified_value.all_weekdays == 4) {
                                $('select[name="weekdays[]"]').find('option[value="' + specified_value.weekdays + '"]').attr('selected', true);
                                $('input[name="ordinal"]').val(specified_value.ordinal);
                            } else if (specified_value.all_weekdays == 0) {
                                $.each(specified_value.weekdays, function (index, value) {
                                    $('select[name="weekdays[]"]').find('option[value="' + value + '"]').attr('selected', true);
                                })
                            }


                            break;
                        default:
                            break;
                    }

                    $('select[name="email_me"]').find('option[value="' + cronJobSettings.email_me + '"]').attr('selected', true);

                    $('select[name="log_output_length"]').find('option[value="' + cronJobSettings.log_output_length + '"]').attr('selected', true);

                    $('#cookies').val(cronJobSettings.cookies);

                    $('#posts').val(cronJobSettings.posts);

                    $('#cron_job_name').val(cronJobSettings.cron_job_name);


                    if (cronJobSettings.group_id && (cronJobSettings.group_id > 0)) {
                        $('select[name="groupId"]').find('option[value="' + cronJobSettings.group_id + '"]').attr('selected', true);
                    }
                }
            }


            if( ! /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
                var $url = $("#cronJobSettings").find('#url');
                var url = $url.val();
                $url.focus().val('').val(url);
            }
         }
    }

    function handleCreateCronJob() {
        $('.create-cron-job').click(function(e){
            $('#cronJobSettings').find('#cronJobSettingsLabel')
                .text('Create Cron Job').end() // headline
                .find('#cronJobSettingsDone')
                .text('Create Cron Job').end() // button
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), cronJobSettingsLoaded);
            e.preventDefault();
        });
    }

    function handleEditCronJob() {
        $('.editAction').click(function(e){
            $('#cronJobSettings').find('#cronJobSettingsLabel')
                .text('Update Cron Job').end()
                .find('#cronJobSettingsDone')
                .text('Update Cron Job').end()
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), cronJobSettingsLoaded);
            e.preventDefault();
        });
    }

    function handleCloneCronJob() {
        $('.cloneAction').click(function(e){
            $('#cronJobSettings').find('#cronJobSettingsLabel')
                .text('Clone Cron Job').end()
                .find('#cronJobSettingsDone')
                .text('Create Cron Job').end()
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), cronJobSettingsLoaded);
            e.preventDefault();
        });
    }
/*
    function handleCloneCronJob() {
        // open ajax clone cron job form
        $('.cloneAction').each(function(index){
            $(this).click(function(){
                if (!$(this).hasClass('active')) {
                    $(this).addClass('active').prev().removeClass('active');
                    $(this).parent().parent().next().hide().next().fadeIn(100);
                } else {
                    $(this).removeClass('active');
                    $(this).parent().parent().next().next().hide();
                }
                return false;
            })        
        });
        
        $('.close-clone-cron-job').click(function() {
            $(this).closest('.cloneCronJobRow').fadeOut(10)
                .prev().prev().find('.cloneAction').removeClass('active');
        })
    }
*/

    function positionTopNotice(notice, type) {
        notice = '<div class="alert alert-' + type + '"><button data-dismiss="alert" class="close" type="button">×</button>' + notice + '</div>';
        $topNotice = $('#topNotice').html(notice);
        $topNotice.css('left', ($(window).width() - $topNotice.width()) / 2);
        $('#topNotice').show();
    }

    function closeLoadingIcon() {
        $('#topNotice').hide();
    }

    function addCommas(n){
        var rx=  /(\d+)(\d{3})/;
        return String(n).replace(/^\d+/, function(w){
            while(rx.test(w)){
                w= w.replace(rx, '$1,$2');
            }
            return w;
        });
    }

    function updateCoinStatistics(coin, coinOccupied) {
        remainingCoins = coin - coinOccupied;
        occupiedPercent = Math.ceil(coinOccupied / coin * 100);
        remainingPercent = 100 - occupiedPercent;
        $('#coinStatistic').find('#totalCoins').text(addCommas(coin)).end()
            .find('#occupiedCoins').text(addCommas(coinOccupied)).end()
            .find('#remainingCoins').text(addCommas(remainingCoins)).end()
            .find('#occupiedPercent').width(occupiedPercent + '%').end()
            .find('#remainingPercent').width(remainingPercent + '%').end();
    }

    function handleSwitch() {
        $('.switch').on('switch-change', function (e, data) {
            cronJobId = $(this).parent().parent().find('td').eq(1).text();
            var $switch = $(this);
            if ((typeof $switch[0].disableSwitchHandler != 'undefined') && $switch[0].disableSwitchHandler) {
                $switch[0].disableSwitchHandler = false;
                return false;
            }
            positionTopNotice('Loading ...', 'info');
            if ($switch.bootstrapSwitch('status')) {
                $.get('/cron/ajaxenable/id/' + cronJobId,
                    function(data){
                        if (data.redirect) {
                            // redirect to login page
                            location.reload();
                        } else if (data.error) {
                            positionTopNotice(data.error, 'error');
                            $switch[0].disableSwitchHandler = true;
                            $switch.bootstrapSwitch('setState', false); 
                        } else if (data.success) {
                            // secceeded
                            positionTopNotice('Cron job (ID: ' + cronJobId + ') has been enabled.', 'success');
                            // update
                            updateCoinStatistics(data.statistics.coin, data.statistics.coin_occupied);
                        } else {
                            // failed, should never reach.
                            alert('An error occured.');
                            $switch[0].disableSwitchHandler = true;
                            $switch.bootstrapSwitch('setState', false); 
                        }
                    },
                    'json'
                );
            } else {
                $.get('/cron/ajaxdisable/id/' + cronJobId,
                    function(data){
                        //closeLoadingIcon();
                        if (data.redirect) {
                            // redirect to login page
                            location.reload();
                        } else if (data.error) {
                            positionTopNotice(data.error, 'error');
                            $switch[0].disableSwitchHandler = true;
                            $switch.bootstrapSwitch('setState', true); 
                        } else if (data.success) {
                            // secceeded
                            positionTopNotice('Cron job (ID: ' + cronJobId + ') has been disabled.', 'success');
                            // update
                            updateCoinStatistics(data.statistics.coin, data.statistics.coin_occupied);
                        } else {
                            // failed, should never reach.
                            alert('An error occured.');
                            $switch[0].disableSwitchHandler = true;
                            $switch.bootstrapSwitch('setState', true); 
                        }
                    },
                    'json'
                );                
            }
            return false;
        });
    }

    function handleTestCronJob() {
        $('.runnowAction').click(function(){
            window.open($(this).attr('data-href'), '_blank');
            window.focus();
        });
    }
    
    function handleResetStat() {
        $('.resetStatAction').click(function(){
            cronJobId = $(this).parent().parent().find('td').eq(1).text();
            var $_this = $(this).parent().parent();
            $.get('/cron/ajaxresetstat/id/' + cronJobId,
                    function(data){
                        if (data.redirect) {
                            // redirect to login page
                            location.reload();
                        } else if (data.error) {
                            positionTopNotice(data.error, 'error');
                        } else if (data.success) {
                            // secceeded
                            positionTopNotice('Statistics reset.', 'success');
                            // update
                            $_this.find('.statTs').text('0').end().find('.statTf').text('0').attr('style', '').end().find('.statCf').text('0');
              
                        } else {
                            // failed, should never reach.
                            alert('An error occured.');
                        }
                    },
                    'json'
                );
        })
    }

    function handleDelete() {
        $('.deleteAction').click(function(){
            cronJobId = $(this).parent().parent().find('td').eq(1).text();
            bootbox.dialog('Are you sure you want to delete the cron job (ID: ' + cronJobId + ') ?', [
                {
                    "label" : "Yes, delete it.",
                    "class" : "btn-u",
                    "callback": function() {
                        $.post('/cron/ajaxdelete/id/' + cronJobId, {submit: "Yes"}, 
                            function(data){

                                if (data.redirect) {
                                    // redirect to login page
                                    location.reload();
                                } else if (data.error) {
                                    positionTopNotice(data.error, 'error');
                                } else if (!isNaN(data)) {
                                    // secceeded
                                    positionTopNotice('Cron job (ID: ' + cronJobId + ') has been deleted. Refreshing page ...', 'success');
                                    // check if there is only one cron job on the page
                                    if ($('.deleteAction').length == 1) {
                                        // check if there is more than one page of cron jobs
                                        if ($('.paginationControl').length) {
                                            newLocation = $('.paginationControl a').eq(0).attr('href');
                                        }
                                    }				

                                    if (typeof newLocation != 'undefined') {
                                        location = newLocation;
                                    } else {
                                        location.reload();
                                    }

                                } else {
                                    // failed, should never reach.
                                    alert('An error occured.');
                                }
                            },
                            'json'
                        );
                    }
                },
                {
                    "label" : "Cancel",
                    "class" : "btn",
                    "callback": function() {                    
                    }
                }
            ], {
                "backdrop" : "static",
                "keyboard" : false,
                "show" : true,
                "animate" : false,
            });
            return false;
        })
    }

    function handleLogs () {
        var handler = function() {
            var left = parseInt($(this).css('left'), 10);
            var temp = left / 600;
            var predictionNumber = Math.ceil(temp * executionNumber);
            $('#predictionNumber').text(predictionNumber + ' prediction(s)');    	
            var logNumber = executionNumber - predictionNumber;
            $('#logNumber').text(logNumber + ' log(s)');    	
            $('input[name="leftPos"]').val(left);
        };	
        $( "#draggable" ).draggable({ 
            axis: "x", 
            containment: "parent",
            drag: handler,
            stop: handler
        });
    }

    function handleOutputDisplay () {
        $('.viewCronJobOutput').live('click', function(){
            $outputRow = $(this).parent().parent().nextAll('.ouutputRow:first');
            if ($outputRow.is(":visible")) {
                $outputRow.hide();
            } else {
                $outputRow.show();
            }
        });
    }
    
    function handleOutputErrorDisplay () {
        $('.viewCronJobOutputError').live('click', function(){
            $outputRow = $(this).parent().parent().nextAll('.outputErrorRow:first');
            if ($outputRow.is(":visible")) {
                $outputRow.hide();
            } else {
                $outputRow.show();
            }
        });
    }

    function handleClickover() {
    	
    	if ($('.pricing-head').length) {
    		var container = 'body';
    	} else {
    		var container = '';
    	}
    	
    	
        $popoverTriggers = $('.popoverTrigger');
        $popoverTriggers.each(function(){
            
            $(this)[0].onTrigger = false;
            $(this)[0].onTip = false;
            var sto, showImmediately;

            $(this).popover({
                html:true,
                trigger: "manual",
                animate: false,
                container: container
                //delay: { show: 0, hide: 0 }
            }).on("click", function(e) {
                e.preventDefault();
            }).on("mouseenter", function() {
                $(this)[0].onTrigger = true;
                var $popover = $(this).next();
                var _this = this;               

                if ((!$popover.hasClass('popover')) || (!$popover.hasClass('in'))) {
                    clearTimeout(sto);
                    showImmediately = setTimeout(function() {
                        $(_this).popover('show').next().on("mouseenter", function() {
                            $(_this)[0].onTip = true;
                        }).on("mouseleave", function() {
                            $(_this)[0].onTip = false;
                            var __this = _this;
                            sto = setTimeout(function() {
                                if ((!$(__this)[0].onTrigger) && (!$(__this)[0].onTip)) {
                                    $(__this).popover("hide");
                                }
                            }, 200);
                        });
                    }, 500);
                }
            }).on("mouseleave", function() {

                clearTimeout(showImmediately);

                $(this)[0].onTrigger = false;
                var _this = this;
                sto = setTimeout(function() {
                    if ((!$(_this)[0].onTrigger) && (!$(_this)[0].onTip)) {
                      $(_this).popover("hide");
                    }
                }, 200);
            });
        });
    }

    function handleShowRows() {
        // change show rows
        $('#showRows').change(function() {
            var cookieName = 'cron';
            if ($('.cronJobListing').length) {
                cookieName = 'cron';
            } else if ($('.affiliatePageList').length) {
                cookieName = 'affiliatePage';
            } else if ($('.commissionList').length) {
               cookieName = 'commission'; 
            } 
            $.cookie(cookieName + '_showrows', $(this).parent().find('option:selected').eq(0).text(), {expires: 30, path: '/'});
            location = $('.paginationControl').attr('data-href');
        })
    }

    function ajaxPost(url, params, $checkedItems, updateMode) {
        $.ajax({
            type: "POST",
            url: url,
            async: false,
            data: params,
            dataType: 'json',
            success: function (data) {
                if (data == null) {
                    return false;
                }

                var emailMes = {'0': 'never', '1': 'if execution fails', '2': 'after execution'};
                
                if (data.redirect) {
                    location.reload();
                } else if (data.type) {
                    positionTopNotice(data.message, data.type);
                    if (data.accountStatistics) {
                        updateCoinStatistics(data.accountStatistics.coin, data.accountStatistics.coin_occupied);
                    }

                    if (updateMode == 5) {
                        // bulk deletion
                        location.reload();
                        return;
                    }

                    if (data.updateCronJobIds) {
                        $checkedItems.each(function(index){
                            $row = $(this).parent().parent();
                            cronJobId = $row.children().eq(1).text();
                            if ($.inArray(cronJobId, data.updateCronJobIds) != -1) {
                                
                                if (updateMode == 1) {
                                    // enable
                                    $switch = $row.find('.switch').eq(0);
                                    $switch[0].disableSwitchHandler = true;                                
                                    $switch.bootstrapSwitch('setState', true);
                                } else if (updateMode == 2) {
                                    // disable
                                    $switch = $row.find('.switch').eq(0);
                                    $switch[0].disableSwitchHandler = true;                                
                                    $switch.bootstrapSwitch('setState', false);
                                } else if (updateMode == 3) {
                                    // email
                                    cronJob = data.updateCronJobs[cronJobId];
                                    $row.find('.coinOccupied').eq(0).text(addCommas(cronJob['coin_occupied']))
                                        .end().end()
                                        .find('.emailMe').eq(0).text(emailMes[cronJob['email_me']]);
/*
                                    $row.next().find('select[name="email_me"]').val(cronJob['email_me'])
                                        .end().next().find('select[name="email_me"]').val(cronJob['email_me']);*/
                                } else if (updateMode == 4) {
                                    // log
                                    cronJob = data.updateCronJobs[cronJobId];
                                    $row.find('.coinOccupied').eq(0).text(addCommas(cronJob['coin_occupied']));

                                    if (cronJob['log_output_length'] == 0) {
                                        temp = 'don\'t log';
                                    } else if (cronJob['log_output_length'] == 10240) {
                                        temp = '<a title="View logs and predictions" href="/cron/log/id/' + cronJobId + '">logs &amp; predictions</a>';
                                    }
                                    $row.find('.logsAndPredictions').eq(0).html(temp);
/*
                                    $row.next().find('select[name="log_output_length"]').val(cronJob['log_output_length'])
                                        .end().next().find('select[name="log_output_length"]').val(cronJob['log_output_length']);*/
                                }
                            }
                        })
                    }
                }
            }
        })
    }

    function handleCheckAll() {
        // multiple check, for all tables
        var $itemTables = $('table.cronList');
        if ($itemTables.length) {
            $itemTables.each(function(i){
                var $itemTable = $(this);
                var itemTable = $(this)[0];

                if (typeof itemTable.$itemCheckboxes == 'undefined') {
                    itemTable.$itemCheckboxes = $itemTable.find('input.itemCheckbox[type="checkbox"]');
                }
                
                itemTable.$itemCheckboxes.change(function(){
                    if ($(this).is(':checked')) {
                        $(this).parent().parent().addClass('rowChecked');
                         // check the checkall checkbox if all rowcheckboxes are checked            
                        if (itemTable.$itemCheckboxes.filter(':checked').length == itemTable.$itemCheckboxes.length) {
                            $itemTable.find('input.checkAll[type="checkbox"]').attr('checked', true);
                        }   
                    } else {
                        $(this).parent().parent().removeClass('rowChecked');
                        // uncheck the checkall checkbox if all rowcheckboxes are unchecked
                        if (itemTable.$itemCheckboxes.filter(':checked').length == 0) {
                            $itemTable.find('input.checkAll[type="checkbox"]').attr('checked', false);
                        }            
                    }
                });

                // wider
                /*itemTable.$itemCheckboxes.each(function(){
                    var _this = this;
                    $(this).parent().click(function(event){
                        if (event.target.nodeName != 'INPUT') {
                            //$(_this).attr("checked", !$(_this).attr("checked"));
                            $(_this).prop("checked", !$(_this).prop("checked"));
                        } else {
                            event.stopPropagation();
                        }
                    });
                });*/

                $itemTable.find('input.checkAll[type="checkbox"]').change(function(){
                    if ($(this).is(':checked')) {
                        itemTable.$itemCheckboxes.attr('checked', true);
                        itemTable.$itemCheckboxes.each(function(){
                            $(this).parent().parent().addClass('rowChecked');
                        })
                    } else {
                        itemTable.$itemCheckboxes.attr('checked', false);
                        itemTable.$itemCheckboxes.each(function(){
                            $(this).parent().parent().removeClass('rowChecked');
                        })
                    }    
                })



                //if (typeof itemTable.$itemGroupCheckboxes == 'undefined') {
                    itemTable.$itemGroupCheckboxes = $itemTable.find('.groupRow input.itemCheckbox[type="checkbox"]');
                //}

                //if (typeof itemTable.$itemCronJobCheckboxes == 'undefined') {
                    itemTable.$itemCronJobCheckboxes = $itemTable.find('.cronJobInGroup input.itemCheckbox[type="checkbox"]');
                //}

                itemTable.$itemCronJobCheckboxes.change(function(){
                    var groupId = $(this).attr('data-inGroup');
                    if ($(this).is(':checked')) {
                        //$(this).parent().parent().addClass('rowChecked');
                         // check the checkall checkbox if all rowcheckboxes are checked            
                        if (itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]:checked').length == itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]').length) {
                            $itemTable.find('[data-groupId="' + groupId + '"] input[type="checkbox"]').attr('checked', true);
                        }   
                    } else {
                        //$(this).parent().parent().removeClass('rowChecked');
                        // uncheck the checkall checkbox if all rowcheckboxes are unchecked
                        if (itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]:checked').length == 0) {
                            $itemTable.find('[data-groupId="' + groupId + '"] input[type="checkbox"]').attr('checked', false);
                        }            
                    }
                });

                itemTable.$itemGroupCheckboxes.change(function(){
                    var groupId = $(this).parent().attr('data-groupId');
                    if ($(this).is(':checked')) {
                        itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]').attr('checked', true);
                        itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]').each(function(){
                            $(this).parent().parent().addClass('rowChecked');
                        })
                    } else {
                        itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]').attr('checked', false);
                        itemTable.$itemCheckboxes.filter('[data-inGroup="' + groupId + '"]').each(function(){
                            $(this).parent().parent().removeClass('rowChecked');
                        })
                    }
                });
            })
        }

        $('select#bulkActionSelect').change(function() {
            var $checkedItems = $('table.cronList input.itemCheckbox[name="ids[]"]:checked');
            switch ($(this).find("option:selected").parent().attr('label')) {
                case 'Update Status':
                    var toStatusId = $(this).val();
                    var count = 0;
                    var params = new Object;
                    $checkedItems.each(function(){
                        cronJobId = $(this).parent().next().text();
                        params['details_' + (count ++)] = cronJobId + ',' + toStatusId;
                    });
                    if (toStatusId == 1) {
                        ajaxPost('/cron/ajaxbulkenable', params, $checkedItems, 1);
                    } else if (toStatusId == 0) {
                        ajaxPost('/cron/ajaxbulkdisable', params, $checkedItems, 2);
                    }
                    break;

                case 'Update Email Notification':
                    var to = $(this).val();
                    var count = 0;
                    var params = new Object;
                    $checkedItems.each(function(){
                        cronJobId = $(this).parent().next().text();
                        params['details_' + (count ++)] = cronJobId + ',' + to;
                    });
                    ajaxPost('/cron/ajaxbulkemail', params, $checkedItems, 3);
                    break;

                // for all tables
                case 'Update Logs & Predictions':
                    var to = $(this).val();
                    var count = 0;
                    var params = new Object;
                    $checkedItems.each(function(){
                        cronJobId = $(this).parent().next().text();
                        params['details_' + (count ++)] = cronJobId + ',' + to;
                    });
                    ajaxPost('/cron/ajaxbulklog', params, $checkedItems, 4);
                    break;

                case 'General':
                    if (confirm('Do you want to permanently delete the selected items?')) {
                        var count = 0;
                        var params = new Object;
                        $checkedItems.each(function(){
                            cronJobId = $(this).parent().next().text();
                            params['details_' + (count ++)] = cronJobId;
                        })

                        ajaxPost('/cron/ajaxbulkdelete', params, $checkedItems, 5);
                    }
                    break;

                default:
                    break;
            }
            // change to default
            $(this).val('Bulk Action');
        })
    }
    
    function handleClock()
    {    
	    function SetTimer()
	    {
	    	timestamp += 1000;
	        var date = new Date(timestamp);
	        timeStr = date.toUTCString().replace('GMT', timezone);
	        if (timeStr.length == 28) {
				timeStr = timeStr.substring(0, 5) + '0' + timeStr.substring(5);
	        }
	        $("#clock").html(timeStr);
	    }
	    if ($("#clock").length) {
	    	setInterval(function(){SetTimer()}, 1000);
	    }
    }

    
    function handleTimeConversion()
    {
        var $times = $(".timeToConvert");
	    if ($times.length) {
            var d = new Date()
            var n = d.getTimezoneOffset() * 60 * 1000;
            $times.each(function(i){
                var date = new Date($(this).attr('data-timestamp') * 1000 - n);
                timeStr = date.toISOString().replace('T', ' ').substring(0, 19);
                $(this).html(timeStr).css('color', '#333333');
            });
	    }
    }

    function handlePlaceholder()
    {
        if (document.createElement("input").placeholder == undefined) {
            $('[placeholder]').focus(function() {
            var input = $(this);
            if (input.val() == input.attr('placeholder')) {
                input.val('');
                input.removeClass('placeholder');
            }
            }).blur(function() {
            var input = $(this);
            if (input.val() == '' || input.val() == input.attr('placeholder')) {
                input.addClass('placeholder');
                input.val(input.attr('placeholder'));
            }
            }).blur();

            $('[placeholder]').parents('form').submit(function() {
                $(this).find('[placeholder]').each(function() {
                    var input = $(this);
                    if (input.val() == input.attr('placeholder')) {
                        input.val('');
                    }
                })
            });
        }
    }

    function isJson(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

    function handleManuallyTest()
    {
        $testResult = $('#cronJobTestResult');
        if ($testResult.length) {
            $.get('/cron/ajaxtestresult/id/' + $testResult.attr('data-cronjobid'),
                function(data){
                    if (isJson(data)) {
                        data = $.parseJSON(data);
                        if (data.redirect) {
                            // redirect to login page
                            location.reload();
                        } else if (data.error) {
                            $testResult.find('td').html(data.error);
                        }
                    } else {
                        // success
                        $testResult.replaceWith(data);
                        handleClickover();
                    }
                }
            );
        }
    }

/*
    function handleLightbox()
    {
        $('.img-modal').click(function(event) {
            $("#img-in-modal").attr("src", $(this).attr('href'));
            $('#myModal').modal('show');
            return false;
        });
    }*/

    function handleClickSchedule()
    {
        $clickSchedule = $('#clickSchedule');
        if ($clickSchedule.length) {
            cronJobSettingsLoaded();
        }    
    }

    function switchToLoadingMode($button)
    {
        if ($button.prop("tagName").toLowerCase() == 'input') {
            $button.attr('data-value', $button.val());
            $button.val('Loading ...');
        } else {
            $button.attr('data-text', $button.text());
            $button.text('Loading ...');
        }
    }

    function exitLoadingMode($button)
    {
        if ($button.prop("tagName").toLowerCase() == 'input') {
            $button.val($button.attr('data-value'));
        } else {
            $button.text($button.attr('data-text'));
        }
    }

    function handleClickScheduleLogin()
    {
        var $clickScheduleLoginForm = $('#clickScheduleLoginForm');
        if ($clickScheduleLoginForm.length) {
            var clickScheduleLoginFormOptions = { 
                beforeSubmit: function(formData, jqForm, validateOptions) {
                    var form = jqForm[0];
                },
                beforeSerialize: function(form, options) {
                    var form = form[0];

                    if (!form.username.value) {
                        alert('You should enter a username.');
                        form.username.focus();
                        return false;
                    }

                    if (!form.password.value) {
                        alert('You should enter a password.');
                        form.password.focus();
                        return false;
                    }
                },
                success: function(data) {
                    if (data.success) {
                        // hide the register and login box, show logged info and a new add cron job btn
                        clearBox(data.success);
                    }  else if (data.error) {
                        positionTopNotice(data.error, 'error');
                    } else {
                        // failed
                        alert(data);
                        return false;
                    }
                },
                dataType: "json",
            };

            $('#clickScheculeLogin').click(function() {                
                // check login
                $.get('/user/loggedin',
                    function(data){
                        if (data.success) {
                            // hide the register and login box, show logged info and a new add cron job btn
                            clearBox(data.success);
                        } else {
                            // not in logged in status, use the entered user info to login
                            $clickScheduleLoginForm.ajaxSubmit(clickScheduleLoginFormOptions); 
                        }
                    },
                    'json'
                );
                // always return false to prevent standard browser submit and page navigation 
                return false; 
            });

            /* 
            $('#clickSchedule .openidLoginBtn').click(function(){
                var link = $(this).attr('href');
                // check login
                $.get('/user/loggedin',
                    function(data){
                        if (data.success) {
                            // hide the register and login box, show logged info and a new add cron job btn
                            clearBox(data.success);
                        } else {
                            // not in logged in status
                            $.get(link,
                                function(data){
                                    if (data.error) {
                                        positionTopNotice(data.error, 'error');
                                    } else if (data.success) {
                                        // hide the register and login box, show logged info and a new add cron job btn
                                        clearBox(data.success);
                                    }
                                },
                                'json'
                            );
                        }
                    },
                    'json'
                );
                return false;
            })*/
        }    
    }


    function handleClickScheduleRegister()
    {
        var $clickScheduleRegisterForm = $('#clickScheduleRegisterForm');
        if ($clickScheduleRegisterForm.length) {
            var clickScheduleRegisterFormOptions = { 
                beforeSubmit: function(formData, jqForm, validateOptions) {
                    var form = jqForm[0];
                },
                beforeSerialize: function(form, options) {
                    quickRegisterFormFieldsValid = true;
                    validateUsername($('.quick-reg input[name="username"]').eq(0), $('.quick-reg input[name="emailAddress"]').eq(0));
                    if (!quickRegisterFormFieldsValid) {
                        exitLoadingMode($('#clickScheduleRegister'));
                        return false;
                    }
                    validateEmail($('.quick-reg input[name="emailAddress"]').eq(0));
                    if (!quickRegisterFormFieldsValid) {
                        exitLoadingMode($('#clickScheduleRegister'));
                        return false;
                    }
                    validatePassword($('.quick-reg input[name="password"]').eq(0));
                    if (!quickRegisterFormFieldsValid) {
                        exitLoadingMode($('#clickScheduleRegister'));
                        return false;
                    }
                },
                success: function(data) {
                    if (data.success) {
                        // hide the register and login box, show logged info and a new add cron job btn
                        clearBox(data.success);
                    }  else if (data.error) {
                        positionTopNotice(data.error, 'error');
                        exitLoadingMode($('#clickScheduleRegister'));
                    } else {
                        // failed
                        alert(data);
                        exitLoadingMode($('#clickScheduleRegister'));
                        return false;
                    }
                },
                dataType: "json",
            };

            $('#clickScheduleRegister').click(function() {

                switchToLoadingMode($(this));

                // check login
                $.get('/user/loggedin',
                    function(data){
                        if (data.success) {
                            // hide the register and login box, show logged info and a new add cron job btn
                            clearBox(data.success);
                        } else {
                            // not in logged in status, use the entered user info to register
                            $clickScheduleRegisterForm.ajaxSubmit(clickScheduleRegisterFormOptions); 
                        }
                    },
                    'json'
                );
                // always return false to prevent standard browser submit and page navigation 
                return false; 
            });            
        }    
    }

    function clearBox(username)
    {
        $('.hideWhenLoggedIn').remove();
        $('#clickScheduleOptions').prepend('<div class="span4 bg-light" style="width: 282px;"><p>You have logged in as <b>' + username + '</b></p><button id="cronJobSettingsDone" class="btn btn-primary">Add Cron Job</button></div>');
        handleCronJobSettings();
        handleCronJobSettings(true);
    }

/*
    function checkLogin()
    {
        $.get('/user/loggedin',
            function(data){
                if (data.success) {
                    // hide the register and login box, show logged info and a new add cron job btn
                    $('.hideWhenLoggedIn').remove();
                    $('<div class="span4 bg-light"><p>You have logged in as <b>' + data.success + '</b></p><button id="cronJobSettingsDone" class="btn btn-primary">Create Cron Job</button></div>').insertBefore('#templateOption');
                    handleCronJobSettings();
                    handleCronJobSettings(true);
                } 
            },
            'json'
        );
    }*/

    function handleAffiliatePageSettings(rightNow) {
        // ajax create affiliate page form
        var affiliatePageCreateOptions = { 
            beforeSubmit: function(formData, jqForm, validateOptions) {
                var form = jqForm[0];
            },
            beforeSerialize: function(form, options) {
                var form = form[0];

                if (!form.affiliatePage.value) {
                    alert('You should enter a URL.');
                    form.affiliatePage.focus();
                    return false;
                } else if ((!isValidUrl(form.affiliatePage.value)) || (form.affiliatePage.value == 'http://')) {
                    alert('The URL you entered is not valid.');
                    form.affiliatePage.focus();
                    return false;
                }

                //url = $(form).attr('action') + query;
                //options['url'] = url;
            },
            success: function(data) {
                if (data.redirect) {
                    // redirect to login page
                    location.reload();
                }  else if (data.error) {
                    positionTopNotice(data.error, 'error');
                } else if (!isNaN(data)) {
                    // secceeded
                    positionTopNotice('Done. Refreshing page ...', 'success');
                    location = '/affiliates';
                } else {
                    // failed
                    alert(data);
                    return false;
                }
            },
            dataType: "json",
        };

        if (typeof rightNow != 'undefined') {
            $('.affiliatePageSetting').ajaxSubmit(affiliatePageCreateOptions); 
        } else {
            $('#affiliatePageSettingsDone').click(function() {
                $('.affiliatePageSetting').ajaxSubmit(affiliatePageCreateOptions); 
                // always return false to prevent standard browser submit and page navigation 
                return false; 
            });
        }
    }

    function affiliatePageSettingsLoaded()
    {
        if ($("#affiliatePageSettings").find('.modal-body').text() == '{"redirect":"\\/user\\/login"}') {
            window.location = '/user/login';
        } else {

            $('#topNotice').hide();

/*
            $('input[name="specifiedBy"]').click(function(){
                switch ($(this).val()) {
                    case '1':
                    case '2':
                        $(this).parent().parent().parent().parent().parent().parent().find('.modal-body .timesAndDates').slideUp('fast');
                        break;
                    case '3':
                        $(this).parent().parent().parent().parent().parent().parent().find('.modal-body .timesAndDates').slideDown('fast');
                        break;
                    default: 
                        break;
                };
            });

            $('select[name="timeInterval"]').focus(function(){
                $('input[name="specifiedBy"][value="1"]').click();
            });

            $('#cron_expression').focus(function(){
                $('input[name="specifiedBy"][value="2"]').click();
            });

            $('.timesAndDates input[type="radio"]').change(function(){
                var name = $(this).attr('data-name');
                var form = $(this).closest('form')[0];
                var ena = ($(this).attr('data-ena') == '1') ? true : false;
                var mode = $(this).attr('data-mode');
                enable_cron_fields(name, form, ena, mode);
            })

            $('input[name="all_minutes_random_times"], input[name="all_hours_random_times"], input[name="all_days_random_times"], input[name="ordinal"]').click(function(){
                $(this).parent().find('input:radio').trigger('click');//attr('checked', true);
            });*/
            

            // if edit view
            if ($('#editView').length) {
                // initialize the eidt form
                if (typeof affiliatePageSettings != 'undefined') {
                    // populate the fields
                    $('#affiliatePage').val(affiliatePageSettings.affiliate_page);
                }
            }


            if( ! /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
                var $url = $("#affiliatePageSettings").find('#affiliatePage');
                var url = $url.val();
                $url.focus().val('').val(url);
            }
         }
    }

    function handleCreateAffiliatePage() {
        $('.add-affiliate-page').click(function(e){
            $('#affiliatePageSettings').find('#affiliatePageSettingsLabel')
                .text('Add Affiliate Page').end() // headline
                .find('#affiliatePageSettingsDone')
                .text('Add Affiliate Page').end() // button
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), affiliatePageSettingsLoaded);
            e.preventDefault();
        });
    }

    function handleEditAffiliatePage() {
        $('.editapAction').click(function(e){
            $('#affiliatePageSettings').find('#affiliatePageSettingsLabel')
                .text('Edit Affiliate Page').end()
                .find('#affiliatePageSettingsDone')
                .text('Update Affiliate Page').end()
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), affiliatePageSettingsLoaded);
            e.preventDefault();
        });
    }

    function handleDeleteAffiliatePage() {
        $('.deleteapAction').click(function(){
            affiliatePageId = $(this).parent().parent().find('td').eq(1).text();
            bootbox.dialog('Are you sure you want to delete the affiliate page (ID: ' + affiliatePageId + ') ? If there is valid commissions that is associated with it, you\'re unable to delete the affiliate page.', [
                {
                    "label" : "Yes, delete it.",
                    "class" : "btn-u",
                    "callback": function() {
                        $.post('/affiliates/ajaxdelete/id/' + affiliatePageId, {submit: "Yes"}, 
                            function(data){

                                if (data.redirect) {
                                    // redirect to login page
                                    location.reload();
                                } else if (data.error) {
                                    positionTopNotice(data.error, 'error');
                                } else if (!isNaN(data)) {
                                    // secceeded
                                    positionTopNotice('Affiliate page (ID: ' + affiliatePageId + ') has been deleted. Refreshing page ...', 'success');
                                    // check if there is only one affiliate page on the page
                                    if ($('.deleteAction').length == 1) {
                                        // check if there is more than one page of affiliate pages
                                        if ($('.paginationControl').length) {
                                            newLocation = $('.paginationControl a').eq(0).attr('href');
                                        }
                                    }				

                                    if (typeof newLocation != 'undefined') {
                                        location = newLocation;
                                    } else {
                                        location.reload();
                                    }

                                } else {
                                    // failed, should never reach.
                                    alert('An error occured.');
                                }
                            },
                            'json'
                        );
                    }
                },
                {
                    "label" : "Cancel",
                    "class" : "btn",
                    "callback": function() {                    
                    }
                }
            ], {
                "backdrop" : "static",
                "keyboard" : false,
                "show" : true,
                "animate" : false,
            });
            return false;
        })
    }

    function handleAffiliatePageCheckAll() {
        // multiple check, for all tables
        var $itemTables = $('table.affiliatePageList');
        if ($itemTables.length) {
            $itemTables.each(function(i){
                var $itemTable = $(this);
                var itemTable = $(this)[0];
                if (typeof itemTable.$itemCheckboxes == 'undefined') {
                    itemTable.$itemCheckboxes = $itemTable.find('input.itemCheckbox[type="checkbox"]');
                }
                
                itemTable.$itemCheckboxes.change(function(){
                    if ($(this).is(':checked')) {
                        $(this).parent().parent().addClass('rowChecked');
                         // check the checkall checkbox if all rowcheckboxes are checked            
                        if (itemTable.$itemCheckboxes.filter(':checked').length == itemTable.$itemCheckboxes.length) {
                            $itemTable.find('input.checkAll[type="checkbox"]').attr('checked', true);
                        }   
                    } else {
                        $(this).parent().parent().removeClass('rowChecked');
                        // uncheck the checkall checkbox if all rowcheckboxes are unchecked            
                        if (itemTable.$itemCheckboxes.filter(':checked').length == 0) {
                            $itemTable.find('input.checkAll[type="checkbox"]').attr('checked', false);
                        }            
                    }
                });

                $itemTable.find('input.checkAll[type="checkbox"]').change(function(){
                    if ($(this).is(':checked')) {
                        itemTable.$itemCheckboxes.attr('checked', true);
                        itemTable.$itemCheckboxes.each(function(){
                            $(this).parent().parent().addClass('rowChecked');
                        })
                    } else {
                        itemTable.$itemCheckboxes.attr('checked', false);
                        itemTable.$itemCheckboxes.each(function(){
                            $(this).parent().parent().removeClass('rowChecked');
                        })
                    }    
                })
            })
        }

        $('select#bulkActionApSelect').change(function() {
            var $checkedItems = $('table.affiliatePageList input.itemCheckbox[type="checkbox"]:checked');
            switch ($(this).find("option:selected").parent().attr('label')) {
                case 'General':
                    if (confirm('Do you want to permanently delete the selected affiliate pages? Note: affiliate pages that have valid commissions will be kept.')) {
                        var count = 0;
                        var params = new Object;
                        $checkedItems.each(function(){
                            apId = $(this).parent().next().text();
                            params['details_' + (count ++)] = apId;
                        })

                        ajaxPost('/affiliates/ajaxbulkdelete', params, $checkedItems, 5);
                    }
                    break;

                default:
                    break;
            }
            // change to default
            $(this).val('Bulk Action');
        })
    }

    function handleGroupView() {
        $('#gvSwitcher').change(function() {
            if ($('#gvSwitcher').is(':checked')) {
                $.cookie('gv', '1', {expires: 30, path: '/'});
            } else {
               $.cookie('gv', '0', {expires: -10, path: '/'});
            }
            location = '/user';
        })
    }


    function handleGroupSettings() {
        // ajax create group form
        var groupCreateOptions = { 
            beforeSubmit: function(formData, jqForm, validateOptions) {
                var form = jqForm[0];
            },
            beforeSerialize: function(form, options) {
                var form = form[0];

                if (!form.groupName.value) {
                    alert('Please enter a group name.');
                    form.groupName.focus();
                    return false;
                }
            },
            success: function(data) {
                if (data.redirect) {
                    // redirect to login page
                    location.reload();
                }  else if (data.error) {
                    positionTopNotice(data.error, 'error');
                } else if (!isNaN(data)) {
                    // secceeded
                    positionTopNotice('Done. Refreshing page ...', 'success');
                    location = '/user';
                } else {
                    // failed
                    alert(data);
                    return false;
                }
            },
            dataType: "json",
        };

        $('#groupSettingsDone').click(function() {
            $('.groupSetting').ajaxSubmit(groupCreateOptions); 
            // always return false to prevent standard browser submit and page navigation 
            return false; 
        });
    }

    function groupSettingsLoaded()
    {
        if ($("#groupSettings").find('.modal-body').text() == '{"redirect":"\\/user\\/login"}') {
            window.location = '/user/login';
        } else {

            $('#topNotice').hide();

            // if edit view
            if ($('#editView').length) {
                // initialize the eidt form
                if (typeof groupSettings != 'undefined') {
                    // populate the fields
                    $('#groupName').val(groupSettings.group_name);
                }
            }


            if( ! /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
                var $url = $("#groupSettings").find('#groupPage');
                var url = $url.val();
                $url.focus().val('').val(url);
            }
         }
    }

    function handleCreateGroup() {
        $('.create-group').click(function(e){
            $('#groupSettings').find('#groupSettingsLabel')
                .text('Create Group').end() // headline
                .find('#groupSettingsDone')
                .text('Create Group').end() // button
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), groupSettingsLoaded);
            e.preventDefault();
        });
    }

    function handleEditGroup() {
        $('.editGroupAction').click(function(e){
            $('#groupSettings').find('#groupSettingsLabel')
                .text('Edit Group').end()
                .find('#groupSettingsDone')
                .text('Update Group').end()
                .on('hidden', function() {
                    $(this).removeData('modal').find('.modal-body').html('<p>Loading ...</p>');
                }).modal("show").find('.modal-body').load($(this).attr("data-href"), groupSettingsLoaded);
            e.preventDefault();
        });
    }

    function handleDeleteGroup() {
        $('.deleteGroupAction').click(function(){
            groupId = $(this).parent().parent().find('td').eq(0).attr('data-groupId');
            bootbox.dialog('Are you sure you want to delete the group (ID: ' + groupId + '). The cron jobs in it will NOT be deleted.', [
                {
                    "label" : "Yes, delete it.",
                    "class" : "btn-u",
                    "callback": function() {
                        $.post('/groups/ajaxdelete/id/' + groupId, {submit: "Yes"}, 
                            function(data){

                                if (data.redirect) {
                                    // redirect to login page
                                    location.reload();
                                } else if (data.error) {
                                    positionTopNotice(data.error, 'error');
                                } else if (!isNaN(data)) {
                                    // secceeded
                                    positionTopNotice('Group (ID: ' + groupId + ') has been deleted. Refreshing page ...', 'success');
                                    location.reload();
                                } else {
                                    // failed, should never reach.
                                    alert('An error occured.');
                                }
                            },
                            'json'
                        );
                    }
                },
                {
                    "label" : "Cancel",
                    "class" : "btn",
                    "callback": function() {                    
                    }
                }
            ], {
                "backdrop" : "static",
                "keyboard" : false,
                "show" : true,
                "animate" : false,
            });
            return false;
        })
    }

    function recalculateGroupCronJobs()
    {
        $('.groupViewCronJobs tbody .groupRow').each(function(index, item){
            var count = $(this).nextUntil('.groupRow').length;
            $(this).find('.cronJobCount').text(count);
            if (count) {
                $(this).find('.groupCronJobCounter').show();
            } else {
                $(this).find('.groupCronJobCounter').hide();
            }
        })
    }

    // sort group
    function handleSortGroup()
    {
        if (typeof gv == 'undefined') {
            return;
        }

        var fixHelper = function(e, ui) {
            ui.children().each(function() {
                $(this).width($(this).width());
            });
            return ui;
        };

        var tbodyFixHelper = function(e, ui) {
            ui.children().eq(0).children().each(function() {
                $(this).width($(this).width());
            });
            return ui;
        };
        
        $("tbody").sortable({
            cursor: "move",
            connectWith: "tbody",		
            items: 'tr:not(".groupRow")',
            
            helper: fixHelper,
            placeholder: "sortable-placeholder",
            forcePlaceholderSize: true,

            start: function (event, ui) {
                ui.placeholder.html('<td colspan="' + ui.item.children().length + '">&nbsp;</td>');
                ui.item.children().css('background-color', '#D5F9B0');
            },
            stop: function( event, ui ) {
                ui.item.children().animate({
                    backgroundColor: "transparent"
                    }, 1000, function(){$(this).css('background', '');});

                // update group id
                var newGroupId = ui.item.parent().find('tr.groupRow .checkboxCol .itemCheckbox').val();
                ui.item.find('.checkboxCol .itemCheckbox').attr('data-inGroup', newGroupId);
                    
                var vals = [];
                ui.item.parent().find('tr.cronJobInGroup .checkboxCol .itemCheckbox').each(function(i){
                    vals[i] = $(this).val();
                });
                vals = $.map(vals, function(n, i) {
                    return n;
                });

                if (ui.item.parent().find('tr.groupRow i.icon-folder-close').length) {
                    ui.item.hide();
                }
                recalculateGroupCronJobs();
/*
                if (vals.length) {
                    ui.item.parent().find('tr.groupRow .cronJobCount').text(vals.length);
                } else {
                    ui.item.parent().find('tr.groupRow .cronJobCount').text(vals.length);
                }*/

                $.post('/cron/sort/', 
                    {
                        cronJobIdInGroup: ui.item.find('.checkboxCol .itemCheckbox').val() + ',' + newGroupId, 
                        cronJobIds: vals.join(',')
                    }, 
                    function(data){
                        if (data.redirect) {
                            // redirect to login page
                            location.reload();
                        } else if (data.error) {
                            positionTopNotice(data.error, 'error');
                        } else if (!isNaN(data)) {
                            // secceeded
                        } else {
                            // failed, should never reach.
                            alert('An error occured.');
                        }
                    },
                    'json'
                );        	
            },
            }).disableSelection();

        $("table").sortable({		
            cursor: "move",
            items: 'tbody:not(.orphans)',
            
            helper: tbodyFixHelper,
            placeholder: "sortable-placeholder",
            forcePlaceholderSize: true,

            start: function (event, ui) {
                ui.placeholder.html('<tr style="background: #D3D3D3;"><td colspan="' + $('.cronList thead th').length + '" style="height: ' + ui.item.height() + 'px; ">&nbsp;</td></tr>');

                ui.item.children().css('background-color', '#D5F9B0');
            },
            stop: function( event, ui ) {                
                ui.item.children().animate({
                    backgroundColor: "transparent"
                }, 1000, function(){$(this).css('background', '');})

                var vals = [];
                ui.item.parent().find('tr.groupRow .checkboxCol .itemCheckbox').each(function(i){
                    vals[i] = $(this).val();
                });
                vals = $.map(vals, function(n, i) {
                    return n;
                });
                $.post('/groups/sort/', 
                    {groupIds: vals.join(',')}, 
                    function(data){
                        if (data.redirect) {
                            // redirect to login page
                            location.reload();
                        } else if (data.error) {
                            positionTopNotice(data.error, 'error');
                        } else if (!isNaN(data)) {
                            // secceeded
                        } else {
                            // failed, should never reach.
                            alert('An error occured.');
                        }
                    },
                    'json'
                );      
            }		
		}).disableSelection();
    }

    function handleAccordion()
    {
        $(function() {
            //var $items = $('.groupViewCronJobs tbody');
            $('.groupViewCronJobs tbody .groupRow .groupCronJobCounter').live('click', function(){
                $children = $(this).parent().parent().nextUntil('.groupRow');
                if ($children.length) {
                    if ($children.eq(0).is(':visible')) {
                        $children.hide();
                        $(this).html($(this).html().replace('Hide', 'Show').replace('open', 'close'));
                        //$(this).html('<i class="icon-folder-close"></i>');
                    } else {
                        $children.show();
                        $(this).html($(this).html().replace('Show', 'Hide').replace('close', 'open'));
                        //$(this).html('<i class="icon-folder-open"></i>');
                    }
                }    
            });
        });
    }

    function sessId()
    {
        $(function() {
            var $sessId = $('input[name="sessId"]');
            if ($sessId.length) {
                $sessId.val('');
            }
        });
    }

    function disableEnterSubmit()
    {
        $('.modal').on("keypress", 'form', function (e) {
            var code = e.keyCode || e.which;
            if (code == 13) {
                e.preventDefault();
                return false;
            }
        });
    }

    return {
        init: function () {
            sessId();
            handleBootstrap();
            handleIEFixes();
            handleFancybox();
            //handleMisc();
            handleSearch();
            handleContactForm();
            disableToggleLink();
            handleCronJobGenerator();
            handleRunTimePredictor();
            handleQuickRegister();
            handleRegister();
            handlePlan();
            //handleTips();
            handleCronJobSettings();
            handleCreateCronJob();
            handleEditCronJob();
            handleCloneCronJob();
            handleSwitch();
            handleTestCronJob();

            handleResetStat();

            handleDelete();
            handleLogs();
            handleOutputDisplay();
            handleOutputErrorDisplay();
            handleClickover();
            handleShowRows();
            handleCheckAll();
            handleClock();
            handleTimeConversion();
            handlePlaceholder();
            handleManuallyTest();

        //  handleManuallySelect();

        //  handleLightbox();

            handleClickSchedule();
            handleClickScheduleLogin();
            handleClickScheduleRegister();

            handleAffiliatePageSettings();
            handleCreateAffiliatePage();
            handleEditAffiliatePage();
            handleDeleteAffiliatePage();
            handleAffiliatePageCheckAll();

            handleGroupView();

            handleGroupSettings();
            handleCreateGroup();
            handleEditGroup();
            handleDeleteGroup();
            //handleGroupCheckAll();

            handleSortGroup();

            handleAccordion();

            disableEnterSubmit();
        }
    };
}();
