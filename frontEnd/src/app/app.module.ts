import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'
import { FormsModule } from '@angular/forms';
import { ToastyModule } from 'ng2-toasty';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavbarTopComponent } from './navbar-top/navbar-top.component';
import { SiderbarLeftComponent } from './siderbar-left/siderbar-left.component';

import { AuthGuard } from './http.service'
import { AuthService } from './http.service';
import { MyWalletComponent } from './my-wallet/my-wallet.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    NavbarTopComponent,
    SiderbarLeftComponent,
    MyWalletComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ToastyModule.forRoot(),
  ],
  providers: [AuthGuard,AuthService,],
  bootstrap: [AppComponent]
})
export class AppModule { }
