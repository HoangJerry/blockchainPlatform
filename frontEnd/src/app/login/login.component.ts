import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  blockChainID :string;
  password :string;
  constructor(private http: HttpService) { }

  ngOnInit() {
  }
  onClickLogin = () =>{
    this.http.listAccount().subscribe((data) => {console.log(data)});
    this.http.signAccount(this.blockChainID,this.password).subscribe((data)=>{console.log(data)});
  }

}
