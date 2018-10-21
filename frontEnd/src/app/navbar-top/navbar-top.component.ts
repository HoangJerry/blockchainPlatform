import { Component, OnInit } from '@angular/core';
import { AuthService, HttpService } from '../http.service'
import { Router } from '@angular/router'
@Component({
  selector: 'app-navbar-top',
  templateUrl: './navbar-top.component.html',
  styleUrls: ['./navbar-top.component.css']
})
export class NavbarTopComponent implements OnInit {
  currentUser :any;
  balance: any;
  constructor(private http: HttpService, private auth: AuthService, private router: Router) { }

  ngOnInit() {
    this.http.currentUser.subscribe(user => {this.currentUser = user;});
    this.http.getBalance().subscribe(balance=> this.balance=balance);
  }
  ngAfterViewInit() {

  }
  onClickLogout = () => {
  	this.auth.logout();
  	this.router.navigate(['/login']);
  }

}
