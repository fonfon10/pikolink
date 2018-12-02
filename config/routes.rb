Rails.application.routes.draw do

  devise_for :users
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)



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




get '/:id' => "shortener/shortened_urls#show"


  root to: "engineers#index"

end
