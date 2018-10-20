import { Component, OnInit } from '@angular/core';
import { HttpService, AuthService } from '../http.service';
import { ToastyService, ToastyConfig, ToastOptions, ToastData } from 'ng2-toasty';
import { Router }                   from '@angular/router'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  blockChainID :string;
  password :string;
  form: number=1;
  constructor(private http: HttpService, 
              private toastyService:ToastyService, 
              private toastyConfig: ToastyConfig,
              private router: Router,
              private auth:AuthService) {
     this.toastyConfig.theme = 'material';
     if (this.auth.isLoggedIn()){
        this.router.navigate(['/dashboard']);
     }
  }

  ngOnInit() {
  }

  onClickLogin = () =>{
    this.http.signAccount(this.blockChainID,this.password).subscribe(
      (data:any) => {
        console.log(data);
        this.auth.login(data.token)
        this.toastyService.success("Login success!");
        this.router.navigate(['/dashboard']);
      },
      (error)=>{
        this.toastyService.error(error.error.detail);
      }
    );
  }

}
