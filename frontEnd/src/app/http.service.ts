import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(private http: HttpClient) {
  }

  listAccount = () => {
    return this.http.post('http://localhost:8080/',{"method": "personal_listAccounts", "params": [],"id": 1});
  }

  signAccount = (account,password) => {
  	console.log(account,password);
  	account = account.toString('hex');
  	console.log(account,password);
  	return this.http.post('http://localhost:8080/',{"method": "personal_sign", "params": [account, account, password],"id": 1})
  }
}
