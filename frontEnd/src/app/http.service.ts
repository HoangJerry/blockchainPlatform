import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot }              from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { ToastyService, ToastyConfig, ToastOptions, ToastData } from 'ng2-toasty';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  user:any;
  headers:HttpHeaders =new HttpHeaders;
  private messageSource = new BehaviorSubject(this.user);
  currentUser = this.messageSource.asObservable();
  constructor(private http: HttpClient) {
    this.headers = this.headers.set('Content-Type', 'application/json; charset=utf-8');
  }

  signAccount = (account?,password?,token?) => {
  	// account = account.toString('hex');
    if (token){
      let headers = this.headers
      headers = headers.set('Authorization','Token '+token)
      return this.http.post('http://localhost:8000/api/user/login/',{},{headers:headers});
    }
    else{
      let data ={
        'block_chain_id':account,
        'password':password
      }
      return this.http.post('http://localhost:8000/api/user/login/',data);

    }
    
  }
  updateUser(message) {
    this.messageSource.next(message);
  }


}

@Injectable()
export class AuthService {
    constructor(private http: HttpService, private toastyService: ToastyService,
        private toastyConfig: ToastyConfig, private router: Router) {
        this.toastyConfig.theme = 'material';
    }

    isLoginSubject: boolean = false;
    async isLoggedIn() {
        await this.hasToken();
        return this.isLoginSubject;
    }

    login(token): void {
        localStorage.setItem('token', token);
        this.isLoginSubject = true;
    }

    logout = () => {
        localStorage.removeItem('token');
        this.isLoginSubject = false;
        localStorage.removeItem('body');
    }

 
    hasToken(): Observable < boolean > {
        return new Observable(observer => {
                if (!localStorage.getItem('token')) {
                    this.isLoginSubject = false;
                    this.router.navigate(['/login']);
                    observer.next(false);
                    observer.complete();
                } else {
                    this.http.signAccount(null, null, localStorage.getItem('token'))
                        .subscribe(
                            (data: any) => {
                                console.log('hehe');
                                this.http.updateUser(data);
                                this.isLoginSubject = true;
                                observer.next(true);
                                observer.complete();
                            },
                            (error) => {
                                console.log('lala');
                                this.toastyService.error(error.error.detail);
                                this.isLoginSubject = false;
                                this.router.navigate(['/login']);
                                observer.next(false);
                                observer.complete();
                            })
                }
            })
      }
}
@Injectable()
export class AuthGuard implements CanActivate {
    constructor(private router: Router, private _auth:AuthService) { }

    canActivate(next:ActivatedRouteSnapshot, state:RouterStateSnapshot): Observable<boolean> {
        // not logged in so redirect to login page with the return url
        return this._auth.hasToken();
        
        
    }
}
