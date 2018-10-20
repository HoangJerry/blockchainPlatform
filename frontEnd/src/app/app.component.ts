import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontEnd';
  currentUrl: string='';

  constructor(private router: Router) {
  	this.router.events.subscribe((e) => {
	  if (e instanceof NavigationEnd) {
	    this.currentUrl = e.url;
	  }
	});
  }

}
