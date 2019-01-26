class DashboardController < ApplicationController

  before_action :authenticate_user!


  def index


	#user = User.find(current_user)
	@owners = current_user.owners

	owners_id = []

	@owners.each do |owner|

		owners_id << owner.id

	end


#    @q = Shortener::ShortenedUrl.where("owner_id IN (?)",owners_id).ransack(params[:q])
    @q = Shortener::ShortenedUrl.where("owner_id IN (?)",owners_id).ransack(owner_firstname_or_owner_lastname_or_owner_company_name_cont: params[:serge])
    @dashboards = @q.result.includes(:owner).order(:owner_id).page params[:page]







  

    #.includes(:unique_key).order(:owner_id).page params[:page]





#  @q = Engineer.where(user_id: current_user.id).ransack(params[:q])
#  @engineers = @q.result.includes(:company).page(params[:page])




#    @links = Shortener::ShortenedUrl.where("owner_id = ?",current_user).paginate(:page => params[:page], :per_page => 15)



#	links = []

#	@engineers.each do |engineer|

#		link = engineer.shortened_urls
#		links = links + link

#	end

#	@links = links.order(:updated_at).page params[:page]





#    @links = Shortener::ShortenedUrl.where("owner_id = ?",current_user).paginate(:page => params[:page], :per_page => 15)

 


 #   @engineers = Engineer.all



 # @q = Engineer.where(user_id: current_user.id).ransack(params[:q])
 # @engineers = @q.result.includes(:company).page(params[:page])





  end
end




      