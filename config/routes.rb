Rails.application.routes.draw do


  resources :companies

  get 'dashboard/show'

  
  resources :engineers do 
    resources :home do 
    end
  end



  resources :home do 
    member do
     put "select", to: "home#select"
    end
   end


  devise_for :users
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)


get '/:id' => "shortener/shortened_urls#show"


  root to: "engineers#index"

end
