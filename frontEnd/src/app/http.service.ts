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

  getBalance = () =>{
    let headers = this.headers
      headers = headers.set('Authorization','Token '+localStorage.getItem('token'))
    return this.http.get('http://localhost:8000/api/user/balance/',{headers:headers});
  }

  getUserInfor = () =>{
    let headers = this.headers
      headers = headers.set('Authorization','Token '+localStorage.getItem('token'))
    return this.http.get('http://localhost:8000/api/user/me/',{headers:headers});
  }

  getUserTestHistory = (condition?) =>{
    if (condition==undefined){
      condition='';
    }
    let headers = this.headers
      headers = headers.set('Authorization','Token '+localStorage.getItem('token'))
    return this.http.get('http://localhost:8000/api/user/history/test/'+condition,{headers:headers});
  }
  updateUserTestHistory = (data) =>{
    let headers = this.headers
    headers = headers.set('Authorization','Token '+localStorage.getItem('token'));
    return this.http.patch('http://localhost:8000/api/user/history/test/update/'+data.id+'/',data,{headers:headers});

  }
  getDoctorTestHistory = () =>{
    let headers = this.headers
      headers = headers.set('Authorization','Token '+localStorage.getItem('token'))
    return this.http.get('http://localhost:8000/api/doctor/history/test/',{headers:headers});
  }
  createTestHistory = (data) =>{
    let headers = this.headers
      headers = headers.set('Authorization','Token '+localStorage.getItem('token'))
    return this.http.post('http://localhost:8000/api/user/history/test/create/',JSON.stringify(data),{headers:headers});
  }

  updateUser(message) {
    let headers = this.headers
    headers = headers.set('Authorization','Token '+localStorage.getItem('token'));
    this.http.patch('http://localhost:8000/api/user/me/',message,{headers:headers}).subscribe(s=>{});
    this.messageSource.next(message);
  }

  getNameOfTest(){
    let headers = this.headers
    headers = headers.set('Authorization','Token '+localStorage.getItem('token'));
    return this.http.get('http://localhost:8000/api/data/name-of-test/',{headers:headers});
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
                                this.http.updateUser(data);
                                this.isLoginSubject = true;
                                observer.next(true);
                                observer.complete();
                            },
                            (error) => {
                                this.toastyService.error(error.error.detail);
                                this.isLoginSubject = false;
                                this.router.navigate(['/login']);
                                observer.next(false);
                                observer.complete();
                            })
                }
            })
      } 
    isDoctor(): Observable < boolean > {
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
                                // console.log(data.role==10);
                                if (data.role==0){
                                  this.http.updateUser(data);
                                  this.isLoginSubject = true;
                                  observer.next(true);
                                  observer.complete(); 
                                }                              
                                if (data.role==10) {
                                  this.router.navigate(['/dashboard']);
                                  observer.next(false);
                                  observer.complete();
                                }                                
                            },
                            (error) => {
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

@Injectable()
export class DoctorGuard implements CanActivate {
    constructor(private router: Router, private _auth:AuthService) { }

    canActivate(next:ActivatedRouteSnapshot, state:RouterStateSnapshot){
        // not logged in so redirect to login page with the return url
        return this._auth.isDoctor();
    }
}
