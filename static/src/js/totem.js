odoo.define('totem_prueba.totem', function(require) {
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
	var allMyEvents = {};
	var event = null;

	// Crear eventos de desplazamiento a la derecha y a la izquierda de los eventos
	/*var TotemMode = AbstractAction.extend ({
		eventTimeout: null,
		i: 0,
		cargada_config: false,
		myCarrousel: null,
		sliderIndex: 0,
		slides : {},
		event: {},
		events: {
			"click #leftArrowButton": _.debounce(function() {
				this.clear();
				this.nextSlide();
			}, 200, true),
			"click #rightArrowButton": _.debounce(function() {
				this.clear();
				this.backSlide();
			}, 200, true),

		},

		start: async function () {
			console.log("START")

			await this.descargarConfigs();
			await this.descargarDatos();
		},

		clear: function() {
			clearTimeout(this.myCarrousel);
			clearTimeout(this.eventimeout);
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
				
				for (let index = 0; index < aux.length; index++)
					aux[index].style.display = "none";
				
				if (self.sliderIndex >= aux.length)
					self.sliderIndex = 0;
				aux[self.sliderIndex].style.display = "block";
				self.sliderIndex++;
				self.myCarrousel = setTimeout(() => {self.config()},res[0].duration*1000); 
			})
			// .catch(function(err){
			// 	console.error(err);
			// 	Promise.reject(err);
			// }) 
		},

		
		descargarConfigs:  async function() {
			let self = this;
			var def = await this._rpc({
				model: 'res.company',
				method: 'search_read',
				args:[[], ['company_qr','company_description','event_duration']],
			})
			.then(function(res) {
				self.datos_company = res[0];
				self.sacar_duration=(self.datos_company.event_duration *1000);
			});
		}, 

		descargarDatos: async function() {
			let self = this;		
			var def =  await this._rpc({
				model: 'totem_general.totem_general',
				method: 'search_read',
			})
			.then(function (res) {
				self.i = 0;
				self.allMyEvents = res;
				console.log("allmyevents: " + self.allMyEvents)
	            self.event = res[self.i];
	            console.log("primer: " + self.event.image_ids);
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

			self.rebootTimeout();
		},

		backSlide: function() {
			let self = this;
			self.i--;

			if (self.i < 0)
				self.i = self.allMyEvents.length - 1;

			self.rebootTimeout();
		},

		rebootTimeout: async function() {
			let self = this;
			// console.log(self.allMyEvents)
			self.event = self.allMyEvents[self.i];
			self.$el.html(QWeb.render("TotemModeMenu", {widget: self}));
			// console.log($(".myImgSlider"))
			 setTimeout(() =>{
			 		$(".o_totem_prueba_totem_mode_footer").html(QWeb.render("ConfigsData", {widget: self.datos_company}));
			 },0);
			console.log("segundo: " + self.event.image_ids);
			setTimeout(() => {self.config();},0);

			self.eventTimeout = setTimeout(function(){
				clearTimeout(self.myCarrousel);
				self.nextSlide();
			},  self.sacar_duration);
		},
	});

	core.action_registry.add('totem_prueba_totem', TotemMode);
	return TotemMode;*/
});