import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MyWalletComponent } from './my-wallet/my-wallet.component';
import { AuthGuard } from './http.service';
const routes: Routes = [

  	{
	    path: '',
	    redirectTo: '/dashboard',
	    pathMatch: 'full',
  	},
	{
		path :'dashboard',
		component: DashboardComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'wallet',
		component: MyWalletComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'login',
		component: LoginComponent
	},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
