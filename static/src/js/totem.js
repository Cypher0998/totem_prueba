odoo.define('totem_definitivo.totem', function(require) {
	// Sentencia para que si o si se ejecute 
	"use strict";

	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var Session = require('web.session');
	var QWeb = core.qweb;
	var _t = core._t;
	var datos_company;
	var duraciones_de_evento;
	var sacar_duration;
	var refreshTime;
	var popUpTime;
	var allMyEvents = {};
	var event = null;

	// Crear eventos de desplazamiento a la derecha y a la izquierda de los eventos
	var TotemMode = AbstractAction.extend ({
		eventTimeout: null,
		i: 0,
		cargada_config: false,
		myCarrousel: null,
		sliderIndex: 0,
		slides : {},
		modalBool: false,
        modalTimer: null,
		events: {
			"click #leftArrowButton": _.debounce(function() {
				this.clear();
				this.nextSlide();
			}, 200, true),
			"click #rightArrowButton": _.debounce(function() {
				this.clear();
				this.backSlide();
			}, 200, true),
			"click .BannerPush": _.debounce(function(){
				var self = this;
                setTimeout(function(){self.modalBool = true;},0);
                console.log("1");
                self.eventTimeout.pause();
                $("#myPopUp").modal({show: true});
                self.modalTimer = setTimeout(function(){
                    if(self.modalBool){
                        $("#myPopUp").modal('hide');
                        $("#myPopUp").on('hidden.bs.modal', function(e){
                            self.eventTimeout.resume()
                            self.modalBool = false;
                        });
                    }
				},self.popUpTime);
			},200, true),

			"click #closeButton": _.debounce(function() {
                var self = this;
                console.log("Esto no entra");
                if(self.modalBool){
                    console.log("2");
                    $("#myPopUp").modal('hide');
                    self.eventTimeout.resume()
                    clearTimeout(self.modalTimer);
                    self.modalBool = false;
                }
            }, 200, true),
            "click #contenedor": _.debounce(function() {
                var self = this;
                console.log("Prueba 1");
                if(self.modalBool){
                    console.log("2");
                    $("#myPopUp").modal('hide');
                    self.eventTimeout.resume()
                    clearTimeout(self.modalTimer);
                    self.modalBool = false;
                }
            }, 200, true),
            "click #cancelarButton": _.debounce(function() {
                var self = this;
                console.log("Prueba 2");
                if(self.modalBool){
                    console.log("2");
                    $("#myPopUp").modal('hide');
                    self.eventTimeout.resume()
                    clearTimeout(self.modalTimer);
                    self.modalBool = false;
                }
            }, 200, true),
        },
        


		start: async function () {
			await this.descargarConfigs();
			await this.descargarDatos();
		},

		clear: function() {
			clearTimeout(this.myCarrousel);
			this.eventTimeout.clearTimeout();
		},
		// Funcion que carga los datos del modelo de totem_general
		config: function() {
			let self = this;
			self.session=Session;
			var def = this._rpc ({
				model: 'res.company',
				method: 'search_read',
				args: [[], ['duration']],
			})
			.then(function (res) {
				console.log()
				self.slides = $(".myImgSlider");
				let aux = self.slides;

				console.log("self.slides", self.slides);
				
				if (aux.length > 0) {
					for (let index = 0; index < aux.length; index++)
						aux[index].style.display = "none";
								
					if (self.sliderIndex >= aux.length)
						self.sliderIndex = 0;
					aux[self.sliderIndex].style.display = "block";
					self.sliderIndex++;
					// if (res[0].duration==0) {
					// 	res[0].duration=4;
					// }
				}
				self.myCarrousel = setTimeout(() => {self.config()},res[0].duration*1000); 
			})
		},

		
		descargarConfigs:  async function() {
			let self = this;
			var def = await this._rpc({
				model: 'res.company',
				method: 'search_read',
				args:[[], ['company_qr','company_description','event_duration',
				'company_refresh_time','company_pop_up_time','company_header_background',
				'company_general_background','company_footer_background',
				'text_color_header','text_color_general','text_color_footer']],
			})
			.then(function(res) {
				self.datos_company = res[0];
				// if (self.datos_company.event_duration==0){
				// 	self.datos_company.event_duration=10;
				// }

				self.sacar_duration=(self.datos_company.event_duration * 1000);

				// if (self.datos_company.company_refresh_time == 0){
				// 	self.datos_company.company_refresh_time = 15;
				// }
				self.refreshTime=(self.datos_company.company_refresh_time * 1000);

				// if(self.datos_company.company_pop_up_time == 0){
				// 	self.datos_company.company_pop_up_time = 35;
				// }
				self.popUpTime = (self.datos_company.company_pop_up_time * 1000);
			});
		}, 

		descargarDatos: async function() {
			let self = this;		
			var def =  await this._rpc({
				model: 'event.event',
				method: 'get_events_by_screen',
				args: [this.getSession().uid, ],
			})
			.then(function (res) {
				clearTimeout(self.myCarrousel);
				const HORAS = 86400000
				let eventsInTime = []
				for (let iterator = 0; iterator < res.length; iterator++){
					let dentro=false;
					console.log("Este es el objeto",res[iterator].my_event_dates);
					res[iterator].my_event_dates.forEach(fechas =>{
						let eventDate = Date.parse(fechas.date);
						let endDate = eventDate;
						if(fechas.final_date!=false)
							endDate = Date.parse(fechas.final_date);
						if(eventDate<=Date.now() && Date.now()<endDate+HORAS){
							let todayTime = new Date(Date.now());
							todayTime = (todayTime.getHours()*60*60*1000)+(todayTime.getMinutes()*60*1000);
							for (let j=0; j<fechas.hour_set.length && dentro==false; j++){
								if(fechas.hour_set[j].initial_hour<=todayTime && todayTime<fechas.hour_set[j].final_hour){
									eventsInTime.push(res[iterator]);
									dentro=true;
								}
							}
						}
					});
				}
				self.i = 0;
				self.allMyEvents = eventsInTime;
	            
	            
	            self.company_description = self.datos_company.company_description;
				self.company_qr = self.datos_company.company_qr;
				self.rebootTimeout();	
			});
		},

		nextSlide: function() {
			let self = this;
			self.i++;

			if (self.i >= self.allMyEvents.length)
				self.i = 0;
			self.clear();
			self.rebootTimeout();
		},

		backSlide: function() {
			let self = this;
			self.i--;

			if (self.i < 0)
				self.i = self.allMyEvents.length - 1;
			self.clear();
			self.rebootTimeout();
		},

		rebootTimeout: async function() {
			let self = this;
			//self.clear();
			// console.log(self.allMyEvents)
			self.event = self.allMyEvents[self.i];
			self.$el.html(QWeb.render("TotemModeMenu", {widget: self}));
			// console.log($(".myImgSlider"))
			 setTimeout(() =>{
			 		$(".o_totem_definitivo_totem_mode_footer").html(QWeb.render("ConfigsData", {widget: self.datos_company}));
			 },0);
			self.backup(self.refreshTime*60);
			setTimeout(() => {self.config();},0);

			self.eventTimeout = new Timer(function(){
				self.clear();
				self.nextSlide();
			},  self.sacar_duration);
		},
        backup: function(tiempo_refresco){
            var self = this;
            setTimeout(() => {
                $("#mymodal").modal('hide');
                $("#mymodal").on('hidden.bs.modal', function(e){
                    if(self.eventTimeout!=null)
                        self.eventTimeout.clearTimeout();
                    clearTimeout(self.modalTimer);
                    self.modalBool = false;
                    self.start();
                });
            }, tiempo_refresco - 1500);
        },
	});

		function Timer(callback, delay) {
        var timerId, start, remaining = delay;
    	let self=this;
        self.pause = function() {
            window.clearTimeout(self.timerId);
            self.remaining -= new Date() - self.start;
        };
    
        self.resume = function() {
            self.start = new Date();
            window.clearTimeout(self.timerId);
            self.timerId = window.setTimeout(callback, remaining);
        };

        self.clearTimeout = function() {
            window.clearTimeout(self.timerId);
        }
    
        self.resume();
    }

	core.action_registry.add('totem_definitivo_totem', TotemMode);
	return TotemMode;
});